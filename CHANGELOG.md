# Changelog

All notable changes to this repository are recorded here.

## Unreleased

- Started an ADR register (`adr/`) and recorded
  [ADR-0001: Repository Merge and History Policy](adr/0001-repository-merge-and-history-policy.md)
  — squash-or-rebase merges (no merge commits) with enforced linear history
  where the plan permits, applied across the active pentaxis93 repositories.
- Added the reusable Fedora CoreOS host-setup baseline:
  `install-fcos.sh`, `fcos-host-setup/setup.sh`, and
  `fcos-host-setup/packages.txt`.
- Added focused tests for the FCOS install script and host-setup script.
- Documented the baseline as a multi-host, consumer-agnostic practice.
- Documented the baseline Layer 2 tooling, including `bw`, Zellij
  `gruvbox-dark` configuration in `config.kdl`, host-wide `EDITOR`/`VISUAL`,
  and Helix `line-number` configuration in `config.toml`.
