# FCOS host dev environment

Reusable dev-environment baseline for Fedora CoreOS hosts.
This directory holds everything a future operator (human or AI) needs to bring
a fresh FCOS host up to the baseline tooling.

## Quick start

```bash
# On the FCOS host as `core`:
git clone git@github.com:pentaxis93/commons.git ~/commons
cd ~/commons/fcos-host-setup

./setup.sh                       # Phase 1: layers Fedora packages (idempotent)
sudo systemctl reboot            # FCOS atomic switch into new deployment

# (reconnect after ~30-60s)
cd ~/commons/fcos-host-setup
./setup.sh                       # Phase 2: user-space binaries + zsh environment

# Then log out and back in so the new default shell takes effect:
exit
ssh <hostname>
# You'll land in a `➜ <hostname> ~` zsh prompt.
```

`setup.sh` is fully idempotent at every step. Running it after both phases
complete is a safe no-op that reports current state.

## Authentication

`git clone git@github.com:...` requires ssh-agent forwarding from your local
workstation. The substrate-coherent pattern is:

- Your **workstation** has ssh-agent running with your GitHub-registered key
  loaded (`ssh-add -l` shows it).
- Your **`~/.ssh/config`** has `ForwardAgent yes` for each FCOS host:
  ```
  Host <host-alias> fcos-*
      ForwardAgent yes
  ```
- On the FCOS host, `ssh -T git@github.com` returns the welcome message,
  confirming the forwarded agent reaches GitHub.

No credentials live on the FCOS host. The workstation is the single point of
truth for your GitHub identity, used in interactive sessions only. Automated
container workloads carry their own credentials independent of this setup.

## Why two phases

FCOS's base OS is an immutable, atomically-managed image. `rpm-ostree install`
stages a new deployment containing the layered packages but does not modify
the running system. A reboot is required to switch into the new deployment.

User-space binaries and shell environment (Phase 2) need the layered tools
(notably `zsh` itself, for `chsh`) and are also more naturally installed once
we're booted into the final environment. Splitting at the reboot boundary
keeps each phase coherent.

## Architecture: three layers

Adding any tool to an FCOS host is a choice between three layers, each with
different properties. The decision per tool is made by what the tool needs
from the system, not by tradition.

### Layer 1 — rpm-ostree (Fedora packages)

For tools that need to be **system citizens**: login shells, expected at
standard system paths, things automation or other tools reach for by absolute
path.

- Defined in `packages.txt`.
- Updates flow through `rpm-ostree upgrade` (auto, via Zincati).
- Each new base image rebases the layer on top — keep the count modest.
- Removed by deleting the line from `packages.txt` and re-running
  `setup.sh`: Phase 1 reconciles the host against the file, uninstalling
  any layered package no longer listed. Takes effect on the next reboot.

### Layer 2 — `~/.local/bin` (static binaries)

For tools that ship as **single static binaries** with their own update story,
or that are not packaged in Fedora repos.

- Lives in `~/.local/bin`, persistent across rpm-ostree upgrades.
- Each tool's update mechanism is appropriate to it (Claude Code auto-updates
  in process; Codex checks at launch; lazygit/lf/bw updated by re-running
  this script).
- `~/.local/bin` is added to zsh's PATH via `~/.zshenv` (see Shell environment
  below).

### Layer 3 — toolbox containers

For **compiling things** or running mutable Fedora environments. Used
ephemerally: `toolbox create <purpose>`, do the work, `toolbox rm <purpose>`.

- **Rule of thumb: toolboxes are for compiling.**
- No persistent toolboxes. Naming and lifecycle are intentional, not implicit.
- Avoids the toolbox-accumulation failure mode where untracked containers pile
  up on the host.

## What's installed

### Layer 1 — rpm-ostree

| Tool         | Purpose                                                  |
|--------------|----------------------------------------------------------|
| `zsh`        | Login shell                                              |
| `helix`      | Modal editor, Rust-based, tree-sitter built in           |
| `git`        | Source control                                           |
| `git-lfs`    | Large-file storage for git                               |
| `git-delta`  | Better git diffs                                         |
| `gh`         | GitHub CLI                                               |
| `ripgrep`    | Fast grep replacement (`rg`)                             |
| `fd-find`    | Friendly find replacement (`fd`)                         |
| `bat`        | `cat` with syntax highlighting                           |
| `lsd`        | `ls` with icons and colors                               |
| `fzf`        | Fuzzy finder                                             |
| `zoxide`     | Smarter `cd` with frecency                               |
| `tree`       | Directory tree visualization                             |
| `htop`       | Interactive process viewer                               |
| `btop`       | Richer system monitor                                    |
| `wget`       | File downloader                                          |
| `unzip`      | ZIP extraction                                           |
| `p7zip`      | 7-Zip support                                            |

`jq` is also required and used (Phase 1's `--json` pending check, Phase 2's
lazygit URL resolution). It's provided by the FCOS base image; not layered.
If a future FCOS version drops it from base, add it to `packages.txt`.

### Layer 2 — `~/.local/bin`

| Tool      | Source                                | Update flow                |
|-----------|---------------------------------------|----------------------------|
| `claude`  | Anthropic native installer            | In-process auto-update     |
| `codex`   | GitHub release static binary          | Launch-time update check   |
| `lazygit` | GitHub release static binary          | Re-run `setup.sh`          |
| `lf`      | GitHub release static binary          | Re-run `setup.sh`          |
| `zellij`  | GitHub release static binary          | Re-run `setup.sh`          |
| `bw`      | Bitwarden Password Manager CLI        | Re-run `setup.sh`          |

`bw` is for interactive operator access to a Bitwarden vault. It is separate
from non-interactive secret-management tooling that a consuming deployment may
install for its own automation.

### Layer 3 — toolbox

None persistent. Create ephemerally if a compile/build task arises.

## Shell environment

Phase 2 produces a fully-configured zsh experience, not just zsh-as-binary.

### Default shell

`zsh` (set via `sudo chsh -s /usr/bin/zsh core`).

### PATH

`~/.zshenv` prepends `~/.local/bin` to PATH. This is necessary because Fedora
ships no `/etc/zprofile` — the `~/.local/bin` entry that bash gets via
`/etc/skel/.bashrc` has no zsh-side equivalent on Fedora/FCOS. `~/.zshenv`
runs for every zsh invocation (interactive, login, non-interactive).

### Editor

`~/.zshenv` also sets `EDITOR` and `VISUAL` to `hx` (Helix). The host ships
with neither set, so editor-spawning apps — git commit messages, `systemctl
edit`, Zellij's `Ctrl-s` `e` scrollback editor — fall back to nano. Setting
the variables once at the environment layer fixes the whole class rather
than per-app.

### Framework

[Oh My Zsh](https://ohmyz.sh) at `~/.oh-my-zsh/`. Installed non-interactively
with `RUNZSH=no CHSH=no` (the script handles `chsh` separately).

### Theme

`robbyrussell`, with a one-line customization to show the short hostname
before the path. Dropped at
`~/.oh-my-zsh/custom/themes/robbyrussell.zsh-theme` — OMZ prefers same-named
files in `custom/themes/` over the core theme, so `ZSH_THEME` stays
`"robbyrussell"`.

Result: `➜  <hostname> ~/commons git:(main)` instead of
`➜  ~/commons git:(main)`.

### Plugins

The canonical pair, cloned to `~/.oh-my-zsh/custom/plugins/`:

- `zsh-autosuggestions` — fish-style command suggestions from history
- `zsh-syntax-highlighting` — colorize valid vs invalid commands as you type

Plus the default `git` plugin enabled by the OMZ-template `.zshrc`.

### Tool integrations

Appended to `~/.zshrc` in a marked block. Each integration is guarded so
absence of a tool doesn't break shell startup:

- **zoxide**: `eval "$(zoxide init zsh)"` — provides `z <pattern>` (jump) and
  `zi` (interactive).
- **fzf**: sources `/usr/share/fzf/shell/key-bindings.zsh` (Ctrl-R history
  search, Alt-C directory jump) and `completion.zsh`.

### Shell helpers

Appended to `~/.zshrc` in a separate marked block from the tool
integrations, so a later addition still lands on a host already past the
integrations marker:

- **`dev <project>`**: enters a Zellij session named for the project,
  creating it if absent (`zellij attach --create`). One named session per
  project keeps the session list legible; `zellij ls` shows them.

### Zellij configuration

`~/.config/zellij/config.kdl` is created if absent, and the theme is
reconciled on every run — so any other Zellij config in the file is left
untouched:

- **`theme "gruvbox-dark"`** — the built-in Zellij theme.

The scrollback editor (`Ctrl-s` then `e`, the smooth way to select and copy
a lot of terminal output) is deliberately *not* set here. Zellij defaults it
to `$EDITOR`, which is set host-wide under [Editor](#editor) above.

### Helix configuration

`~/.config/helix/config.toml` is created if absent, and one setting is
reconciled on every run — so any other Helix config in the file is left
untouched:

- **`line-number = "relative"`** (under the `[editor]` table) — hybrid
  relative line numbers: the current line shows its absolute number, every
  other line shows its distance from it.

## Why this set — decision log

**Default posture: don't add tools.** Each entry above earned its place by
serving a concrete use case in SSH dev work. The following were considered
and rejected:

- **`tmux`** — replaced by Zellij (Layer 2). Zellij serves the same role —
  persistent multiplexed sessions on the host — but its discoverable
  keybindings and built-in session manager remove the friction of tmux's
  modal chords. Zellij is not in the Fedora repos, so it lives in Layer 2
  as a GitHub-release static binary, not here.
- **`tailscale`** — was in use, dropped when mesh networking was retired. Can
  re-add if the need returns.
- **`pass`, `gnupg2`** — credential management belongs on local machines, not
  the server.
- **`podman-compose`** — application workloads run via Quadlet, not compose.
- **`atuin`** — shell history sync; not in current use.
- **`chezmoi`** — we don't manage server dotfiles cross-host. setup.sh handles
  the minimal config that needs to exist; the operator's local chezmoi
  manages workstation dotfiles separately.

When a candidate tool surfaces, the question to ask: *what specific SSH work
does this enable that nothing already installed can?* If the answer is fuzzy,
the answer is no.

## Phase detection logic

`setup.sh` always runs Phase 1, which reconciles the host's layered
packages against `packages.txt` — installing any missing and uninstalling
any that are layered but no longer listed. It then queries
`rpm-ostree status --json` for any deployment with `.staged == true`:

- **If a staged deployment exists**: Phase 1 staged package changes
  (additions, removals, or both). Prompt the
  operator to reboot, then exit. Re-running after reboot continues with
  Phase 2.
- **If no staged deployment exists**: all packages are already layered into
  the booted deployment. Proceed directly to Phase 2.

The `.staged` boolean is the canonical signal that `rpm-ostree install` has
queued a deployment for next boot. It's reliable across rpm-ostree versions
and host states (fresh FCOS with no rollback, host with prior layered state,
host with rollback target — all classified correctly).

Earlier versions of this check parsed text output and assumed pending
deployments are always listed first. That assumption failed on fresh FCOS
hosts where the booted deployment is listed first. `--json` removes the
ambiguity.

Phase 2 is itself idempotent — each install function checks for existing
presence before downloading. The plugin-clones and zshrc-edits use
existence checks and marker-line guards.

## Adding or changing tools

1. Edit `packages.txt` (Layer 1) or `setup.sh` (Layer 2 or shell environment).
2. Run `./setup.sh` on each host to apply.
3. Commit the change to this baseline with rationale in the commit message
   and (if non-trivial) an entry in this README's decision log.

The change is encoded once, applied to all hosts.

## Future direction

Two natural extensions, not yet undertaken:

- **Per-host overrides**: if consuming hosts ever diverge in tooling needs,
  we'd add a hostname-keyed mechanism — e.g.
  `packages-${HOSTNAME}.txt` merged into the base list.
- **Ignition-time bootstrap**: once `setup.sh` is mature and stable, its
  Phase 1 commands could be lifted into the Butane/Ignition config so that
  first-boot produces a fully-layered host without manual intervention.
  Phase 2 (user-space binaries + shell environment) is harder to encode
  declaratively and would likely stay in this script regardless.

Neither is urgent. The current shape is honest about what we know.
