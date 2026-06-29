# commons

Cross-cutting conventions, best practices, and reusable patterns for the
pentaxis93 projects.

A practice belongs here when it has demonstrated benefit and applies across
more than one project — not necessarily everywhere, but broadly enough to be
worth carrying from one project to the next. This is the home for that kind of
durable, shared practice.

## Contents

- [`ONTOLOGY.md`](ONTOLOGY.md) — the ontology of the shared-knowledge body: its
  two hierarchies (stature and authority), the five strata and where each lives,
  and how the two compose. The map for locating any asset's band, and the
  generalization of `pentaxis93/principles`'s `ONTOLOGY.md` up one level.
- [`adr/`](adr/) — architectural decision records for cross-cutting decisions
  that apply across more than one pentaxis93 project. See the
  [register](adr/README.md) for the index.
- [`golden-rules/`](golden-rules/) — domain-specific architectural rules,
  rooted in principle and master-curated. See the
  [register](golden-rules/README.md) for what a golden rule is, how it cites
  the universals beneath it, and the stratum's members.
- [`DEPLOYMENT-DOCUMENTATION-DISCIPLINE.md`](DEPLOYMENT-DOCUMENTATION-DISCIPLINE.md)
  — how a deployment (a host) is documented: what a deployment's documentation
  must contain, what makes it usable rather than merely descriptive, and how it
  relates to the shared baseline a host is built from.
- [`install-fcos.sh`](install-fcos.sh) and
  [`fcos-host-setup/`](fcos-host-setup/) — a reusable Fedora CoreOS host-setup
  baseline for installing FCOS from rescue mode and applying the baseline SSH
  development environment on a fresh host.
