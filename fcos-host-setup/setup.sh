#!/usr/bin/env bash
# FCOS host dev environment setup.
#
# Idempotent installer for the reusable dev-environment baseline on FCOS
# hosts. Architecture and tool rationale are documented in README.md.
#
# Usage:
#   ./setup.sh
#
# Behavior:
#
#   Phase 1 (always runs, idempotent): reconcile the host's layered
#   packages with packages.txt — install any missing, uninstall any that
#   are layered but no longer listed. packages.txt is authoritative. If
#   the reconcile staged a new deployment, prompt for reboot and exit.
#
#   Phase 2 (runs if no pending deployment after Phase 1): install
#   user-space binaries to ~/.local/bin (claude, codex, lazygit, lf,
#   zellij, bw), set zsh as the default login shell.
#
# Re-running is always safe — both phases detect existing state and
# only do the work that's missing.

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Location & helpers
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES_FILE="${SCRIPT_DIR}/packages.txt"

log()  { printf '\n\033[1;34m▶\033[0m %s\n' "$*"; }
ok()   { printf '  \033[1;32m✓\033[0m %s\n' "$*"; }
warn() { printf '  \033[1;33m⚠\033[0m %s\n' "$*"; }
err()  { printf '  \033[1;31m✗\033[0m %s\n' "$*" >&2; }

require_file() {
    if [[ ! -f "$1" ]]; then
        err "required file not found: $1"
        exit 1
    fi
}

# True if a deployment is staged for next boot.
#
# Uses rpm-ostree's structured --json output and queries the explicit
# .staged boolean on each deployment. A "staged" deployment is one that
# rpm-ostree install has queued for next boot. The booted deployment has
# .staged == false (it's already active). A rollback deployment has
# .staged == false (it's neither active nor pending).
#
# This replaces an earlier text-parsing approach that assumed pending
# deployments are always listed first in the text status output. That
# assumption held on a host with prior layered state but failed on a
# fresh FCOS host with no rollback, where the booted deployment was
# listed first and the staged second. jq is in the FCOS base image, so
# it's always available — including before any layered packages are
# applied. (Phase 1 itself surfaces this with "jq (already provided by
# jq-X-Y.fc44.x86_64)" in its Inactive requests message.)
pending_deployment_exists() {
    rpm-ostree status --json 2>/dev/null \
        | jq -e 'any(.deployments[]; .staged == true)' >/dev/null 2>&1
}

# True if zsh is currently the default login shell for $USER.
zsh_is_default() {
    getent passwd "$USER" | cut -d: -f7 | grep -q zsh
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 1: rpm-ostree layer (always runs, idempotent)
# ─────────────────────────────────────────────────────────────────────────────

phase1() {
    log "Phase 1 — reconciling host layered packages with packages.txt"
    require_file "$PACKAGES_FILE"

    local packages
    packages=$(grep -Ev '^\s*(#|$)' "$PACKAGES_FILE" | tr '\n' ' ')

    echo "  Packages requested:"
    # shellcheck disable=SC2086
    for p in $packages; do printf '    %s\n' "$p"; done
    echo

    # --idempotent: don't fail if some packages are already requested.
    # shellcheck disable=SC2086
    sudo rpm-ostree install --idempotent $packages

    # Reconcile removals. packages.txt is authoritative: a package that is
    # layered on the host (booted deployment's requested-packages) but no
    # longer listed in packages.txt is uninstalled, so re-running setup.sh
    # converges the host to the file. The install above only adds; this
    # closes the removal half. Both stage into one pending deployment, so
    # the reboot check in main() still gates a single reboot.
    #
    # Scope: only repo-package overlays (requested-packages) are reconciled.
    # Base-package overrides (rpm-ostree override remove) and local-rpm
    # installs are deliberately untouched — they are not expressible in
    # packages.txt and not this script's concern.
    local layered to_remove pkg
    layered=$(rpm-ostree status --json 2>/dev/null \
        | jq -r '.deployments[] | select(.booted == true)
                 | (."requested-packages" // [])[]')
    to_remove=()
    while IFS= read -r pkg; do
        [[ -z "$pkg" ]] && continue
        # Surrounding spaces make this a whole-word membership test,
        # so e.g. `git` does not spuriously match inside `git-lfs`.
        if [[ " $packages " != *" $pkg "* ]]; then
            to_remove+=("$pkg")
        fi
    done <<< "$layered"

    if [[ ${#to_remove[@]} -gt 0 ]]; then
        warn "Layered packages no longer in packages.txt — uninstalling:"
        for pkg in "${to_remove[@]}"; do printf '    %s\n' "$pkg"; done
        sudo rpm-ostree uninstall "${to_remove[@]}"
    else
        ok "No layered packages to remove; host matches packages.txt."
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: user-space binaries
# ─────────────────────────────────────────────────────────────────────────────

install_claude() {
    if command -v claude >/dev/null 2>&1; then
        ok "claude: $(claude --version 2>&1 | head -1)"
        return
    fi
    log "Installing Claude Code (native installer, in-process auto-update)"
    curl -fsSL https://claude.ai/install.sh | bash
}

install_codex() {
    if command -v codex >/dev/null 2>&1; then
        ok "codex: $(codex --version 2>&1 | head -1)"
        return
    fi
    log "Installing Codex CLI (static binary, launch-time update check)"
    local arch tmp
    arch=$(uname -m)
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/codex.tar.gz" \
        "https://github.com/openai/codex/releases/latest/download/codex-${arch}-unknown-linux-musl.tar.gz"
    tar -xzf "$tmp/codex.tar.gz" -C "$tmp"
    install -m 755 "$tmp/codex-${arch}-unknown-linux-musl" "$HOME/.local/bin/codex"
    rm -rf "$tmp"
}

install_lazygit() {
    if command -v lazygit >/dev/null 2>&1; then
        ok "lazygit: $(lazygit --version 2>&1 | head -1)"
        return
    fi
    log "Installing lazygit (static binary; re-run setup.sh to update)"
    local asset_url tmp
    # lazygit filename embeds version (lazygit_X.Y.Z_linux_x86_64.tar.gz),
    # so we use the GitHub API to resolve the asset URL.
    asset_url=$(curl -fsSL "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" \
                | jq -r '.assets[] | select(.name | endswith("_linux_x86_64.tar.gz")) | .browser_download_url')
    if [[ -z "$asset_url" || "$asset_url" == "null" ]]; then
        err "could not resolve lazygit release asset URL"
        return 1
    fi
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/lazygit.tar.gz" "$asset_url"
    tar -xzf "$tmp/lazygit.tar.gz" -C "$tmp" lazygit
    install -m 755 "$tmp/lazygit" "$HOME/.local/bin/lazygit"
    rm -rf "$tmp"
}

install_lf() {
    if command -v lf >/dev/null 2>&1; then
        ok "lf: $(lf -version 2>&1 | head -1)"
        return
    fi
    log "Installing lf (static binary; re-run setup.sh to update)"
    local tmp
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/lf.tar.gz" \
        https://github.com/gokcehan/lf/releases/latest/download/lf-linux-amd64.tar.gz
    tar -xzf "$tmp/lf.tar.gz" -C "$tmp" lf
    install -m 755 "$tmp/lf" "$HOME/.local/bin/lf"
    rm -rf "$tmp"
}

install_zellij() {
    if command -v zellij >/dev/null 2>&1; then
        ok "zellij: $(zellij --version 2>&1 | head -1)"
        return
    fi
    log "Installing zellij (static binary; re-run setup.sh to update)"
    local arch tmp
    # Zellij release assets are version-stable (no version in the filename),
    # so the predictable latest/download/ URL works without an API lookup.
    # uname -m reports x86_64, which matches the asset's target triple.
    arch=$(uname -m)
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/zellij.tar.gz" \
        "https://github.com/zellij-org/zellij/releases/latest/download/zellij-${arch}-unknown-linux-musl.tar.gz"
    tar -xzf "$tmp/zellij.tar.gz" -C "$tmp"
    install -m 755 "$tmp/zellij" "$HOME/.local/bin/zellij"
    rm -rf "$tmp"
}

install_bw() {
    if command -v bw >/dev/null 2>&1; then
        ok "bw: $(bw --version 2>&1 | head -1)"
        return
    fi
    log "Installing Bitwarden CLI (native binary; re-run setup.sh to update)"
    local tmp
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/bw.zip" \
        "https://vault.bitwarden.com/download/?app=cli&platform=linux"
    unzip "$tmp/bw.zip" -d "$tmp"
    install -m 755 "$tmp/bw" "$HOME/.local/bin/bw"
    rm -rf "$tmp"
}

set_default_shell() {
    if zsh_is_default; then
        ok "default shell: zsh"
        return
    fi
    log "Setting default shell to zsh"
    # On FCOS, core has passwordless sudo; chsh requires sudo for non-self changes.
    sudo chsh -s /usr/bin/zsh "$USER"
    warn "Shell change takes effect on next SSH login."
}

# Ensure ~/.local/bin is on PATH in zsh login shells.
#
# Fedora's /etc/profile (sourced for bash login shells) leads to ~/.local/bin
# being added to PATH via /etc/skel/.bashrc. Fedora ships no /etc/zprofile,
# so the equivalent path for zsh login shells is empty: the user-space
# binaries from Phase 2 (claude, codex, lazygit, lf, bw) are installed but
# unreachable from a fresh zsh SSH session.
#
# Fix: drop a minimal ~/.zshenv that prepends ~/.local/bin to PATH using
# zsh's typeset -U path idiom (deduplicates and prepends in one move).
# Idempotent via a marker line.
ensure_zsh_path() {
    local zshenv="$HOME/.zshenv"
    local marker="# fcos-host-setup: PATH"
    if [[ -f "$zshenv" ]] && grep -qF "$marker" "$zshenv"; then
        ok "~/.zshenv already configures ~/.local/bin on PATH"
        return
    fi
    log "Configuring ~/.zshenv: prepend ~/.local/bin to PATH for zsh"
    cat >> "$zshenv" <<'ZSHENV'

# fcos-host-setup: PATH
# Fedora ships no /etc/zprofile, so zsh login shells don't inherit the
# ~/.local/bin entry that bash gets via /etc/skel/.bashrc. Add it here.
typeset -U path
path=("$HOME/.local/bin" $path)
ZSHENV
}

# Set EDITOR/VISUAL in ~/.zshenv so Helix is the editor for every app that
# spawns one — git commit messages, `systemctl edit`, Zellij's `Ctrl-s e`
# scrollback editor, and so on. The host ships with neither variable set,
# so editor-spawning apps fall back to nano; this fixes that at the source
# rather than per-app. ~/.zshenv runs for every zsh invocation, so the
# variables are present in interactive and non-interactive shells alike.
# Own marker, separate from the PATH block, so this lands on hosts already
# past that marker.
ensure_editor_env() {
    local zshenv="$HOME/.zshenv"
    local marker="# fcos-host-setup: editor"
    if [[ -f "$zshenv" ]] && grep -qF "$marker" "$zshenv"; then
        ok "~/.zshenv already sets EDITOR/VISUAL"
        return
    fi
    log "Configuring ~/.zshenv: set EDITOR/VISUAL to hx (Helix)"
    cat >> "$zshenv" <<'ZSHENV'

# fcos-host-setup: editor
# Helix is the editor for every app that spawns one. VISUAL is checked
# before EDITOR by many tools, so set both.
export EDITOR="hx"
export VISUAL="hx"
ZSHENV
}

# Install Oh My Zsh framework (default robbyrussell theme).
#
# RUNZSH=no: don't spawn an interactive zsh at the end of the install
# CHSH=no:   we already set the default shell in set_default_shell()
install_oh_my_zsh() {
    if [[ -d "$HOME/.oh-my-zsh" ]]; then
        ok "oh-my-zsh: already installed"
        return
    fi
    log "Installing Oh My Zsh (default theme: robbyrussell)"
    RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
}

# Install the canonical extension pair under ~/.oh-my-zsh/custom/plugins/.
# These are not enabled until configure_zshrc() adds them to plugins=(...).
install_zsh_plugins() {
    local custom="$HOME/.oh-my-zsh/custom/plugins"
    if [[ ! -d "$HOME/.oh-my-zsh" ]]; then
        warn "oh-my-zsh not installed; skipping plugin install"
        return 1
    fi
    mkdir -p "$custom"

    local plugins=(
        "zsh-autosuggestions https://github.com/zsh-users/zsh-autosuggestions"
        "zsh-syntax-highlighting https://github.com/zsh-users/zsh-syntax-highlighting.git"
    )

    for entry in "${plugins[@]}"; do
        local name="${entry%% *}"
        local url="${entry#* }"
        if [[ -d "$custom/$name" ]]; then
            ok "$name: present"
        else
            log "Cloning $name"
            git clone --depth 1 "$url" "$custom/$name"
        fi
    done
}

# Configure ~/.zshrc:
#   1. Enable the installed custom plugins in the plugins=(...) array
#   2. Append tool integrations (zoxide init, fzf key-bindings & completion)
#   3. Append shell helpers (the `dev` Zellij-session function)
#
# All edits are idempotent. Plugin entries are added individually only if
# missing; the tool-integration and shell-helper blocks are each gated by
# their own marker comment, so a later-added block still lands on a host
# that already has the earlier ones.
configure_zshrc() {
    local zshrc="$HOME/.zshrc"
    if [[ ! -f "$zshrc" ]]; then
        warn "~/.zshrc not found (oh-my-zsh install should have created it)"
        return 1
    fi

    # 1. Enable plugins by adding any missing ones to plugins=(...)
    local needed=(zsh-autosuggestions zsh-syntax-highlighting)
    local missing=()
    for plugin in "${needed[@]}"; do
        if ! grep -qE "^plugins=\([^)]*\b$plugin\b" "$zshrc"; then
            missing+=("$plugin")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        log "Enabling plugins: ${missing[*]}"
        for plugin in "${missing[@]}"; do
            # Insert plugin name before the closing paren of plugins=(...)
            sed -i "s/^\(plugins=([^)]*\))/\1 $plugin)/" "$zshrc"
        done
    else
        ok "~/.zshrc plugins list complete"
    fi

    # 2. Append tool integrations
    #
    # Each marked block below is skip-or-append (if/else), never early
    # return: a return here would short-circuit every block that follows.
    # New blocks are added the same way — own marker, own if/else.
    local marker="# fcos-host-setup: tool integrations"
    if grep -qF "$marker" "$zshrc"; then
        ok "~/.zshrc tool integrations present"
    else
        log "Appending tool integrations to ~/.zshrc (zoxide, fzf)"
        cat >> "$zshrc" <<'ZSHRC'

# fcos-host-setup: tool integrations
# Hooks the layered modern-Unix tools into the shell. Each guarded so
# absence of a tool doesn't break shell startup.

# zoxide: smarter cd with frecency. `z <pat>` jumps, `zi` interactive.
if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init zsh)"
fi

# fzf: Ctrl-R history search and Alt-C directory jump.
# Fedora installs the shell integration files under /usr/share/fzf/shell/.
[[ -f /usr/share/fzf/shell/key-bindings.zsh ]] && source /usr/share/fzf/shell/key-bindings.zsh
[[ -f /usr/share/fzf/shell/completion.zsh ]]   && source /usr/share/fzf/shell/completion.zsh
ZSHRC
    fi

    # 3. Append shell helpers
    #
    # Own marker, separate from the tool-integrations block, so this block
    # lands on a host already past the integrations marker. Skip-or-append
    # for the same reason as above.
    local helpers_marker="# fcos-host-setup: shell helpers"
    if grep -qF "$helpers_marker" "$zshrc"; then
        ok "~/.zshrc shell helpers present"
    else
        log "Appending shell helpers to ~/.zshrc (dev)"
        cat >> "$zshrc" <<'ZSHRC'

# fcos-host-setup: shell helpers

# dev: enter a Zellij session by project name, creating it if absent.
# `attach --create` is idempotent — attaches if the session exists,
# creates it otherwise — so the same command works for both cases and
# every session is named for its project. `zellij ls` lists them.
dev() { zellij attach --create "${1:-main}"; }
ZSHRC
    fi
}

# Ensure a single-line top-level KDL setting `key "value"` in a config file.
# If a `key ...` line already exists it is replaced in place; otherwise the
# setting is appended. Idempotent: re-running converges the line to `value`
# without ever duplicating it — which a plain append could not guarantee for
# a structured file. Scoped to single-line scalar settings (the form the two
# Zellij settings below take); not for block-valued KDL nodes.
ensure_kdl_setting() {
    local file="$1" key="$2" value="$3"
    local line="$key \"$value\""
    if grep -qxF "$line" "$file"; then
        ok "zellij: $key already \"$value\""
    elif grep -qE "^[[:space:]]*${key}[[:space:]]" "$file"; then
        log "zellij: updating $key -> \"$value\""
        sed -i "s|^[[:space:]]*${key}[[:space:]].*|${line}|" "$file"
    else
        log "zellij: setting $key -> \"$value\""
        printf '%s\n' "$line" >> "$file"
    fi
}

# Configure ~/.config/zellij/config.kdl with the baseline Zellij
# theme. The file is created with a header on first run; the theme setting
# is then reconciled (replace-or-append), so any other Zellij config the
# operator adds is left untouched.
#
#   theme  gruvbox-dark  built-in Zellij theme
#
# The scrollback editor (`Ctrl-s e`) is intentionally not set here: Zellij
# defaults it to $EDITOR, which ensure_editor_env sets host-wide. Setting
# it here too would be a redundant per-app fix for a host-level gap.
configure_zellij() {
    local zdir="$HOME/.config/zellij"
    local cfg="$zdir/config.kdl"
    mkdir -p "$zdir"

    if [[ ! -f "$cfg" ]]; then
        log "Creating ~/.config/zellij/config.kdl"
        cat > "$cfg" <<'KDL'
// Zellij configuration.
//
// `theme` below is managed by fcos-host-setup and
// reconciled on every setup.sh run. Other Zellij settings may be added
// to this file freely; they are left untouched.
KDL
    fi

    ensure_kdl_setting "$cfg" "theme" "gruvbox-dark"
}

# Configure ~/.config/helix/config.toml with the baseline Helix
# settings. The file is created with a header on first run; the managed
# setting is then reconciled, so other Helix config the operator adds is
# left untouched.
#
#   [editor] line-number = "relative"   hybrid relative line numbers
#
# Unlike the Zellij theme (a top-level node), this setting is TOML-table-
# scoped: line-number must sit under [editor]. The reconcile covers all
# four states — already set; a line-number line present (replace it); an
# [editor] table present without the key (insert after the header); or no
# [editor] table at all (append the table).
configure_helix() {
    local hdir="$HOME/.config/helix"
    local cfg="$hdir/config.toml"
    local setting='line-number = "relative"'
    mkdir -p "$hdir"

    if [[ ! -f "$cfg" ]]; then
        log "Creating ~/.config/helix/config.toml"
        cat > "$cfg" <<'TOML'
# Helix configuration.
#
# The [editor] line-number setting is managed by fcos-host-setup and
# reconciled on every setup.sh run. Other Helix settings may be added to
# this file freely; they are left untouched.
TOML
    fi

    if grep -qxF "$setting" "$cfg"; then
        ok "helix: line-number already \"relative\""
    elif grep -qE '^[[:space:]]*line-number[[:space:]]*=' "$cfg"; then
        log "helix: updating line-number -> \"relative\""
        sed -i "s|^[[:space:]]*line-number[[:space:]]*=.*|${setting}|" "$cfg"
    elif grep -qE '^\[editor\]' "$cfg"; then
        log "helix: setting line-number -> \"relative\" under [editor]"
        sed -i "/^\[editor\]/a ${setting}" "$cfg"
    else
        log "helix: adding [editor] table with line-number -> \"relative\""
        printf '\n[editor]\n%s\n' "$setting" >> "$cfg"
    fi
}

# Install a custom robbyrussell theme that shows the hostname.
#
# A file at ~/.oh-my-zsh/custom/themes/<name>.zsh-theme overrides the core
# OMZ theme of the same name without changing ZSH_THEME. Adds %m (short
# hostname) in magenta before the existing %c (current dir name).
#
# This makes which-host-am-I-on obvious in every prompt when operating more
# than one FCOS host.
customize_robbyrussell_theme() {
    local theme="$HOME/.oh-my-zsh/custom/themes/robbyrussell.zsh-theme"
    if [[ -f "$theme" ]]; then
        ok "robbyrussell custom theme present"
        return
    fi
    if [[ ! -d "$HOME/.oh-my-zsh" ]]; then
        warn "oh-my-zsh not installed; skipping theme customization"
        return 1
    fi
    log "Installing customized robbyrussell theme (with hostname)"
    mkdir -p "$(dirname "$theme")"
    cat > "$theme" <<'THEME'
# fcos-host-setup: robbyrussell variant with hostname.
#
# OMZ loads ~/.oh-my-zsh/custom/themes/<name>.zsh-theme in preference to
# the core theme of the same name. Adds %m (short hostname, magenta)
# before %c (current dir name, cyan) so a fresh SSH session shows which
# host the prompt is on.

PROMPT="%(?:%{$fg_bold[green]%}%1{➜%} :%{$fg_bold[red]%}%1{➜%} ) %{$fg[magenta]%}%m %{$fg[cyan]%}%c%{$reset_color%}"
PROMPT+=' $(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%}) "
THEME
}

phase2() {
    log "Phase 2 — installing user-space binaries to ~/.local/bin"
    mkdir -p "$HOME/.local/bin"

    install_claude
    install_codex
    install_lazygit
    install_lf
    install_zellij
    install_bw
    set_default_shell
    ensure_zsh_path
    ensure_editor_env
    install_oh_my_zsh
    install_zsh_plugins
    configure_zshrc
    configure_zellij
    configure_helix
    customize_robbyrussell_theme

    echo
    log "Phase 2 complete. Verify with:"
    cat <<'EOF'

    hx --version
    claude --version
    codex --version
    lazygit --version
    lf -version
    zellij --version
    bw --version

EOF
}

# ─────────────────────────────────────────────────────────────────────────────
# Main: Phase 1 always runs; Phase 2 runs only if no reboot is pending.
# ─────────────────────────────────────────────────────────────────────────────

main() {
    phase1

    if pending_deployment_exists; then
        echo
        log "New deployment staged. Reboot required before Phase 2."
        cat <<EOF

  Next steps:
    1. Inspect:  rpm-ostree status
    2. Reboot:   sudo systemctl reboot
    3. After reboot, re-run this script for Phase 2.

EOF
        exit 0
    fi

    ok "All packages already layered in booted deployment. Continuing."
    phase2
}

main "$@"
