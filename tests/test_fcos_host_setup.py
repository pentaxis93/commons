from pathlib import Path
import os
import stat
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fcos-host-setup" / "setup.sh"
README = ROOT / "fcos-host-setup" / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"


class FcosHostSetupTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "calls.log"

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_executable(self, path, contents):
        path.write_text(textwrap.dedent(contents).lstrip(), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def link_system_tool(self, name):
        target = Path("/usr/bin") / name
        if not target.exists():
            target = Path("/bin") / name
        os.symlink(target, self.bin / name)

    def write_installed_tool(self, name, version_output):
        self.write_executable(
            self.bin / name,
            f"""
            #!/bin/sh
            printf '%s\\n' '{version_output}'
            """,
        )

    def write_host_tool_stubs(self):
        for name in ("cat", "cut", "dirname", "grep", "head", "install", "mkdir", "mktemp", "pwd", "rm", "sed", "tr"):
            self.link_system_tool(name)
        self.write_executable(
            self.bin / "sudo",
            """
            #!/bin/sh
            printf 'sudo %s\\n' "$*" >> "$TEST_CALL_LOG"
            exit 0
            """,
        )
        self.write_executable(
            self.bin / "rpm-ostree",
            """
            #!/bin/sh
            if [ "${1:-}" = "status" ]; then
                printf '{"deployments":[{"staged":false}]}\\n'
                exit 0
            fi
            printf 'rpm-ostree %s\\n' "$*" >> "$TEST_CALL_LOG"
            exit 0
            """,
        )
        self.write_executable(
            self.bin / "getent",
            """
            #!/bin/sh
            printf 'core:x:1000:1000:Core User:%s:/usr/bin/zsh\\n' "$HOME"
            """,
        )
        self.write_executable(
            self.bin / "jq",
            """
            #!/bin/sh
            # Drain stdin first, as real jq does: otherwise exiting before the
            # upstream `rpm-ostree status` stub finishes writing the pipe races
            # it into SIGPIPE, which under `set -o pipefail` surfaced as a flaky
            # 141 exit from Phase 1's `layered=$(... | jq -r ...)` reconcile.
            cat >/dev/null 2>&1
            # `jq -e` is the staged-deployment probe (pending_deployment_exists):
            # exiting 1 reports "nothing staged", so Phase 2 proceeds. Any other
            # invocation is Phase 1's removal-reconcile query, which against this
            # stub's rpm-ostree status yields no layered packages (empty, exit 0).
            case "${1:-}" in
                -e) exit 1 ;;
                *)  exit 0 ;;
            esac
            """,
        )
        self.write_executable(
            self.bin / "git",
            """
            #!/bin/sh
            printf 'git %s\\n' "$*" >> "$TEST_CALL_LOG"
            exit 0
            """,
        )

    def write_bw_download_stubs(self):
        self.write_executable(
            self.bin / "curl",
            """
            #!/bin/sh
            printf 'curl %s\\n' "$*" >> "$TEST_CALL_LOG"
            output=""
            previous=""
            for arg in "$@"; do
                if [ "$previous" = "-o" ]; then
                    output="$arg"
                fi
                previous="$arg"
            done
            [ -n "$output" ] || exit 0
            case "$*" in
                *"https://vault.bitwarden.com/download/?app=cli&platform=linux"*)
                    printf 'fake zip\\n' > "$output"
                    ;;
                *)
                    printf 'unexpected curl: %s\\n' "$*" >&2
                    exit 2
                    ;;
            esac
            """,
        )
        self.write_executable(
            self.bin / "unzip",
            """
            #!/bin/sh
            printf 'unzip %s\\n' "$*" >> "$TEST_CALL_LOG"
            archive="$1"
            shift
            destination=""
            previous=""
            for arg in "$@"; do
                if [ "$previous" = "-d" ]; then
                    destination="$arg"
                fi
                previous="$arg"
            done
            [ -n "$destination" ] || exit 2
            [ -f "$archive" ] || exit 2
            printf '#!/bin/sh\\nprintf "2026.4.1\\\\n"\\n' > "$destination/bw"
            /bin/chmod 755 "$destination/bw"
            """,
        )

    def run_setup(self):
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(self.home),
                "PATH": str(self.bin),
                "TEST_CALL_LOG": str(self.log),
                "USER": "core",
            }
        )
        return subprocess.run(
            ["/usr/bin/bash", str(SCRIPT)],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_phase2_installs_bw_from_official_linux_native_download(self):
        for name, version_output in {
            "claude": "claude 1.0.0",
            "codex": "codex 1.0.0",
            "lazygit": "lazygit 1.0.0",
            "lf": "lf 1.0.0",
            "zellij": "zellij 1.0.0",
        }.items():
            self.write_installed_tool(name, version_output)
        (self.home / ".oh-my-zsh" / "custom" / "plugins").mkdir(parents=True)
        (self.home / ".oh-my-zsh" / "custom" / "themes").mkdir(parents=True)
        (self.home / ".zshrc").write_text("plugins=(git)\n", encoding="utf-8")
        self.write_host_tool_stubs()
        self.write_bw_download_stubs()

        result = self.run_setup()

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        bw = self.home / ".local" / "bin" / "bw"
        self.assertTrue(bw.exists(), "expected bw to be installed to ~/.local/bin/bw")
        self.assertTrue(os.access(bw, os.X_OK), "expected installed bw to be executable")
        log = self.log.read_text(encoding="utf-8")
        self.assertIn("https://vault.bitwarden.com/download/?app=cli&platform=linux", log)
        self.assertIn("bw --version", result.stdout)

    def test_docs_describe_bw_as_fcos_layer2_binary(self):
        readme = README.read_text(encoding="utf-8")
        changelog = CHANGELOG.read_text(encoding="utf-8")

        self.assertIn("### Layer 2 — `~/.local/bin`", readme)
        self.assertIn("`bw`", readme)
        self.assertIn("Bitwarden Password Manager CLI", readme)
        self.assertIn("non-interactive secret-management tooling", readme)
        self.assertIn("bw", changelog)

    def _scaffold_for_phase2(self):
        for name, version_output in {
            "claude": "claude 1.0.0",
            "codex": "codex 1.0.0",
            "lazygit": "lazygit 1.0.0",
            "lf": "lf 1.0.0",
            "zellij": "zellij 1.0.0",
        }.items():
            self.write_installed_tool(name, version_output)
        (self.home / ".oh-my-zsh" / "custom" / "plugins").mkdir(parents=True)
        (self.home / ".oh-my-zsh" / "custom" / "themes").mkdir(parents=True)
        (self.home / ".zshrc").write_text("plugins=(git)\n", encoding="utf-8")
        self.write_host_tool_stubs()
        self.write_bw_download_stubs()

    def test_phase2_configures_zellij_theme(self):
        self._scaffold_for_phase2()

        result = self.run_setup()

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        cfg = self.home / ".config" / "zellij" / "config.kdl"
        self.assertTrue(cfg.exists(), "expected ~/.config/zellij/config.kdl to be created")
        text = cfg.read_text(encoding="utf-8")
        self.assertIn('theme "gruvbox-dark"', text)
        # The scrollback editor is sourced from $EDITOR, not pinned in config.
        self.assertNotIn("scrollback_editor", text)

    def test_phase2_zellij_config_replaces_stale_theme_and_keeps_operator_config(self):
        self._scaffold_for_phase2()
        # Pre-existing config: stale theme plus operator settings — including a
        # scrollback_editor the operator may set themselves — that must all
        # survive untouched, since configure_zellij manages only the theme.
        zdir = self.home / ".config" / "zellij"
        zdir.mkdir(parents=True)
        cfg = zdir / "config.kdl"
        cfg.write_text(
            'theme "nord"\nscrollback_editor "vim"\nmouse_mode true\n',
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        text = cfg.read_text(encoding="utf-8")
        # Theme replaced in place — exactly once, no duplication.
        self.assertEqual(text.count("theme "), 1, text)
        self.assertIn('theme "gruvbox-dark"', text)
        self.assertNotIn("nord", text)
        # Settings configure_zellij does not manage are left untouched.
        self.assertIn('scrollback_editor "vim"', text)
        self.assertIn("mouse_mode true", text)

    def test_phase2_sets_editor_env_in_zshenv(self):
        self._scaffold_for_phase2()

        first = self.run_setup()
        self.assertEqual(first.returncode, 0, f"stdout:\n{first.stdout}\nstderr:\n{first.stderr}")
        zshenv = self.home / ".zshenv"
        self.assertTrue(zshenv.exists(), "expected ~/.zshenv to exist")
        text = zshenv.read_text(encoding="utf-8")
        self.assertIn('export EDITOR="hx"', text)
        self.assertIn('export VISUAL="hx"', text)

        # Marker-gated: a second run must not append the block again.
        second = self.run_setup()
        self.assertEqual(second.returncode, 0, f"stdout:\n{second.stdout}\nstderr:\n{second.stderr}")
        text = zshenv.read_text(encoding="utf-8")
        self.assertEqual(text.count('export EDITOR="hx"'), 1, text)

    def test_docs_describe_zellij_configuration(self):
        readme = README.read_text(encoding="utf-8")
        changelog = CHANGELOG.read_text(encoding="utf-8")

        self.assertIn("config.kdl", readme)
        self.assertIn("gruvbox-dark", readme)
        self.assertIn("EDITOR", readme)
        self.assertIn("gruvbox-dark", changelog)
        self.assertIn("EDITOR", changelog)

    def test_phase2_configures_helix_relative_line_numbers(self):
        self._scaffold_for_phase2()

        first = self.run_setup()
        self.assertEqual(first.returncode, 0, f"stdout:\n{first.stdout}\nstderr:\n{first.stderr}")
        cfg = self.home / ".config" / "helix" / "config.toml"
        self.assertTrue(cfg.exists(), "expected ~/.config/helix/config.toml to be created")
        text = cfg.read_text(encoding="utf-8")
        self.assertIn("[editor]", text)
        self.assertIn('line-number = "relative"', text)

        # Idempotent: a second run must not duplicate the setting.
        second = self.run_setup()
        self.assertEqual(second.returncode, 0, f"stdout:\n{second.stdout}\nstderr:\n{second.stderr}")
        text = cfg.read_text(encoding="utf-8")
        self.assertEqual(text.count('line-number = "relative"'), 1, text)

    def test_phase2_helix_inserts_line_number_under_existing_editor_table(self):
        self._scaffold_for_phase2()
        # Pre-existing config: an [editor] table with an operator key but no
        # line-number, plus a later sub-table. line-number must be inserted
        # under [editor], not leak into [editor.cursor-shape].
        hdir = self.home / ".config" / "helix"
        hdir.mkdir(parents=True)
        cfg = hdir / "config.toml"
        cfg.write_text(
            '[editor]\ncursorline = true\n\n[editor.cursor-shape]\ninsert = "bar"\n',
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        text = cfg.read_text(encoding="utf-8")
        self.assertIn('line-number = "relative"', text)
        # Inserted directly under the [editor] header, before the operator key.
        self.assertIn('[editor]\nline-number = "relative"', text)
        # Operator config preserved untouched.
        self.assertIn("cursorline = true", text)
        self.assertIn("[editor.cursor-shape]", text)
        self.assertIn('insert = "bar"', text)

    def test_phase2_helix_replaces_stale_line_number_value(self):
        self._scaffold_for_phase2()
        hdir = self.home / ".config" / "helix"
        hdir.mkdir(parents=True)
        cfg = hdir / "config.toml"
        cfg.write_text(
            '[editor]\nline-number = "absolute"\nbufferline = "always"\n',
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        text = cfg.read_text(encoding="utf-8")
        self.assertEqual(text.count('line-number = "relative"'), 1, text)
        self.assertIn('line-number = "relative"', text)
        self.assertNotIn("absolute", text)
        self.assertIn('bufferline = "always"', text)

    def test_docs_describe_helix_configuration(self):
        readme = README.read_text(encoding="utf-8")
        changelog = CHANGELOG.read_text(encoding="utf-8")

        self.assertIn("config.toml", readme)
        self.assertIn('line-number = "relative"', readme)
        self.assertIn("config.toml", changelog)
        self.assertIn("line-number", changelog)
