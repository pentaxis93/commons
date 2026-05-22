from pathlib import Path
import os
import stat
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "install-fcos.sh"


class InstallFcosScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "calls.log"
        self.ignition_config = self.root / "test-host-fcos.ign"
        self.ignition_config.write_text("test ignition\n", encoding="utf-8")
        self.write_stub_tools()

    def tearDown(self):
        self.tmpdir.cleanup()

    def run_script(self, *, scenario="ovh", confirm=True, isolated_path=False, args=None):
        env = os.environ.copy()
        path = str(self.bin) if isolated_path else f"{self.bin}:{env['PATH']}"
        env.update(
            {
                "PATH": path,
                "TEST_CALL_LOG": str(self.log),
                "TEST_SCENARIO": scenario,
            }
        )
        if args is None:
            args = [self.ignition_config.name]
        return subprocess.run(
            ["/usr/bin/bash", str(SCRIPT), *args],
            cwd=self.root,
            env=env,
            input="\n" if confirm else "",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def write_executable(self, path, contents):
        path.write_text(textwrap.dedent(contents).lstrip(), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def log_text(self):
        if not self.log.exists():
            return ""
        return self.log.read_text(encoding="utf-8")

    def write_required_tool_placeholders(self, *, absent=(), non_executable=()):
        required = [
            "awk",
            "basename",
            "cp",
            "curl",
            "dd",
            "findmnt",
            "ls",
            "lsblk",
            "mkdir",
            "mount",
            "partx",
            "python3",
            "sleep",
            "umount",
            "xzcat",
        ]
        absent = set(absent)
        non_executable = set(non_executable)
        for name in required:
            path = self.bin / name
            if name in absent:
                if path.exists():
                    path.unlink()
                continue
            path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            mode = path.stat().st_mode
            if name in non_executable:
                path.chmod(mode & ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH)
            else:
                path.chmod(mode | stat.S_IXUSR)

    def write_stub_tools(self):
        self.write_executable(
            self.bin / "findmnt",
            r"""
            #!/usr/bin/env bash
            set -eu
            case "${TEST_SCENARIO:?}" in
              findmnt-cannot-execute) exit 126 ;;
              unresolved-root) exit 1 ;;
              *) echo "/dev/sda1" ;;
            esac
            """,
        )
        self.write_executable(
            self.bin / "lsblk",
            r"""
            #!/usr/bin/env bash
            set -eu
            scenario="${TEST_SCENARIO:?}"
            if [ "$#" -eq 0 ]; then
              case "$scenario" in
                no-persistent)
                  cat <<'OUT'
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda       8:0    0  2.9G  0 disk
sda1      8:1    0  2.9G  0 part /
OUT
                  ;;
                multiple-persistent)
                  cat <<'OUT'
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda       8:0    0  2.9G  0 disk
sda1      8:1    0  2.9G  0 part /
sdb       8:16   0   75G  0 disk
sdc       8:32   0   75G  0 disk
OUT
                  ;;
                nvme)
                  cat <<'OUT'
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda           8:0    0  2.9G  0 disk
sda1          8:1    0  2.9G  0 part /
nvme0n1     259:0    0   75G  0 disk
nvme0n1p3   259:3    0  384M  0 part
OUT
                  ;;
                blank-target)
                  cat <<'OUT'
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda       8:0    0  2.9G  0 disk
sda1      8:1    0  2.9G  0 part /
sdb       8:16   0   75G  0 disk
OUT
                  ;;
                *)
                  cat <<'OUT'
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda       8:0    0  2.9G  0 disk
sda1      8:1    0  2.9G  0 part /
sdb       8:16   0   75G  0 disk
sdb1      8:17   0 73.9G  0 part
sdb13     8:29   0 1023M  0 part
sdb14     8:30   0    4M  0 part
sdb15     8:31   0  106M  0 part
OUT
                  ;;
              esac
              exit 0
            fi

            refreshed() {
              [ -f "${TEST_CALL_LOG:?}" ] &&
                grep -q "^partx --delete $1$" "$TEST_CALL_LOG" &&
                grep -q "^partx --add $1$" "$TEST_CALL_LOG"
            }

            added() {
              [ -f "${TEST_CALL_LOG:?}" ] &&
                grep -q "^partx --add $1$" "$TEST_CALL_LOG"
            }

            disk_partitions() {
              local disk="$1"
              case "$scenario:$disk" in
                blank-target:/dev/sdb)
                  if added /dev/sdb; then
                    printf '/dev/sdb disk\n/dev/sdb1 part\n/dev/sdb2 part\n/dev/sdb3 part\n/dev/sdb4 part\n'
                  else
                    printf '/dev/sdb disk\n'
                  fi
                  ;;
                *:/dev/sdb)
                  if refreshed /dev/sdb; then
                    printf '/dev/sdb disk\n/dev/sdb1 part\n/dev/sdb2 part\n/dev/sdb3 part\n/dev/sdb4 part\n'
                  else
                    printf '/dev/sdb disk\n/dev/sdb1 part\n/dev/sdb13 part\n/dev/sdb14 part\n/dev/sdb15 part\n'
                  fi
                  ;;
                *:/dev/nvme0n1)
                  if refreshed /dev/nvme0n1; then
                    printf '/dev/nvme0n1 disk\n/dev/nvme0n1p1 part\n/dev/nvme0n1p2 part\n/dev/nvme0n1p3 part\n/dev/nvme0n1p4 part\n'
                  else
                    printf '/dev/nvme0n1 disk\n/dev/nvme0n1p1 part\n/dev/nvme0n1p13 part\n/dev/nvme0n1p14 part\n/dev/nvme0n1p15 part\n'
                  fi
                  ;;
                *)
                  echo "unexpected lsblk disk: $disk" >&2
                  exit 2
                  ;;
              esac
            }

            case "$*" in
              "-no PKNAME /dev/sda1")
                echo "sda"
                ;;
              "-dnrpo NAME,TYPE")
                case "$scenario" in
                  no-persistent) printf '/dev/sda disk\n' ;;
                  multiple-persistent) printf '/dev/sda disk\n/dev/sdb disk\n/dev/sdc disk\n' ;;
                  nvme) printf '/dev/sda disk\n/dev/nvme0n1 disk\n' ;;
                  *) printf '/dev/sda disk\n/dev/sdb disk\n' ;;
                esac
                ;;
              "-nrpo NAME,TYPE /dev/sdb")
                disk_partitions /dev/sdb
                ;;
              "-nrpo NAME,TYPE /dev/nvme0n1")
                disk_partitions /dev/nvme0n1
                ;;
              "-nrpo NAME,TYPE,PARTN /dev/sdb")
                echo "lsblk: unknown column: PARTN" >&2
                exit 1
                ;;
              "-nrpo NAME,TYPE,PARTN /dev/nvme0n1")
                echo "lsblk: unknown column: PARTN" >&2
                exit 1
                ;;
              *)
                echo "unexpected lsblk args: $*" >&2
                exit 2
                ;;
            esac
            """,
        )
        self.write_executable(
            self.bin / "curl",
            r"""
            #!/usr/bin/env bash
            set -eu
            case "${*: -1}" in
              https://builds.coreos.fedoraproject.org/streams/stable.json)
                cat <<'JSON'
{"architectures":{"x86_64":{"artifacts":{"metal":{"formats":{"raw.xz":{"disk":{"location":"https://example.invalid/fcos.raw.xz"}}}}}}}}
JSON
                ;;
              https://example.invalid/fcos.raw.xz)
                printf 'compressed-image'
                ;;
              *)
                echo "unexpected curl args: $*" >&2
                exit 2
                ;;
            esac
            """,
        )
        self.write_executable(
            self.bin / "xzcat",
            r"""
            #!/usr/bin/env bash
            set -eu
            cat
            """,
        )
        for name in ["dd", "mount", "mkdir", "cp", "ls", "umount", "sleep"]:
            self.write_executable(
                self.bin / name,
                f"""
                #!/usr/bin/env bash
                set -eu
                printf '{name} %s\\n' "$*" >> "${{TEST_CALL_LOG:?}}"
                cat >/dev/null || true
                """,
            )
        self.write_executable(
            self.bin / "partx",
            r"""
            #!/usr/bin/env bash
            set -eu
            printf 'partx %s\n' "$*" >> "${TEST_CALL_LOG:?}"
            case "${TEST_SCENARIO:?}:$*" in
              blank-target:"--delete /dev/sdb")
                echo "partx: /dev/sdb: cannot delete partitions" >&2
                exit 1
                ;;
              partx-delete-fails:"--delete /dev/sdb")
                echo "partx: /dev/sdb: kernel refused partition delete" >&2
                exit 1
                ;;
            esac
            """,
        )

    def test_ovh_rescue_layout_writes_to_persistent_vps_disk(self):
        result = self.run_script(scenario="ovh")

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        log = self.log_text()
        self.assertIn("dd of=/dev/sdb bs=4M status=progress", log)
        self.assertIn("partx --delete /dev/sdb", log)
        self.assertIn("partx --add /dev/sdb", log)
        self.assertIn("mount /dev/sdb3 /mnt", log)
        self.assertIn(f"cp {self.ignition_config.name} /mnt/ignition/config.ign", log)
        self.assertIn("Detected rescue disk: /dev/sda", result.stdout)
        self.assertIn("Target persistent disk: /dev/sdb", result.stdout)

    def test_blank_target_adds_fcos_partitions_without_deleting_missing_entries(self):
        result = self.run_script(scenario="blank-target")

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        log = self.log_text()
        self.assertIn("dd of=/dev/sdb bs=4M status=progress", log)
        self.assertNotIn("partx --delete /dev/sdb", log)
        self.assertIn("partx --add /dev/sdb", log)
        self.assertIn("mount /dev/sdb3 /mnt", log)

    def test_partition_refresh_stops_when_existing_partition_delete_fails(self):
        result = self.run_script(scenario="partx-delete-fails")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("kernel refused partition delete", result.stderr)
        log = self.log_text()
        self.assertIn("dd of=/dev/sdb bs=4M status=progress", log)
        self.assertIn("partx --delete /dev/sdb", log)
        self.assertNotIn("partx --add /dev/sdb", log)
        self.assertNotIn("mount ", log)

    def test_nvme_target_mounts_partition_three_with_nvme_partition_path(self):
        result = self.run_script(scenario="nvme")

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        log = self.log_text()
        self.assertIn("dd of=/dev/nvme0n1 bs=4M status=progress", log)
        self.assertIn("mount /dev/nvme0n1p3 /mnt", log)

    def test_no_persistent_disk_fails_before_destructive_write(self):
        result = self.run_script(scenario="no-persistent")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("could not identify a persistent target disk", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_multiple_persistent_disks_fail_before_destructive_write(self):
        result = self.run_script(scenario="multiple-persistent")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ambiguous persistent target disks", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_unresolved_rescue_disk_fails_before_destructive_write(self):
        result = self.run_script(scenario="unresolved-root")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("could not identify the rescue disk mounted at /", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_required_tool_execution_failure_names_tool_before_destructive_write(self):
        result = self.run_script(scenario="findmnt-cannot-execute")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required tool findmnt could not execute", result.stderr)
        self.assertNotIn("could not identify the rescue disk mounted at /", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_missing_ignition_config_fails_before_destructive_write(self):
        self.ignition_config.unlink()

        result = self.run_script(scenario="ovh")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"{self.ignition_config.name} is required", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_missing_ignition_argument_fails_before_destructive_write(self):
        result = self.run_script(scenario="ovh", args=[])

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage: install-fcos.sh <ignition-config>", result.stderr)
        self.assertIn("ignition config path is required", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_extra_ignition_argument_fails_before_destructive_write(self):
        result = self.run_script(scenario="ovh", args=[self.ignition_config.name, "extra.ign"])

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage: install-fcos.sh <ignition-config>", result.stderr)
        self.assertIn("expected exactly one ignition config path", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_help_describes_parameterized_invocation_without_writing_disk(self):
        result = self.run_script(scenario="ovh", args=["--help"])

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertIn("Usage: install-fcos.sh <ignition-config>", result.stdout)
        self.assertIn("Install Fedora CoreOS", result.stdout)
        self.assertNotIn("dd ", self.log_text())

    def test_missing_required_tool_names_tool_before_destructive_write(self):
        self.write_required_tool_placeholders(absent={"partx"})

        result = self.run_script(scenario="ovh", isolated_path=True)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required tool partx was not found in PATH", result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_non_executable_required_tool_names_tool_before_destructive_write(self):
        self.write_required_tool_placeholders(non_executable={"partx"})

        result = self.run_script(scenario="ovh", isolated_path=True)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required tool partx is not executable", result.stderr)
        self.assertIn(str(self.bin / "partx"), result.stderr)
        self.assertNotIn("dd ", self.log_text())

    def test_script_does_not_silently_suppress_tool_errors(self):
        script = SCRIPT.read_text(encoding="utf-8")

        self.assertNotIn("2>/dev/null || true", script)
