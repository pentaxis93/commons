# Conventions Register

Domain-specific conventions for the pentaxis93 projects. This register is the
index; each convention is authoritative for its own content once fleshed.

A **convention** is a master-curated, domain-specific choice — a standing answer
for a language, a framework, or a coding practice, **rooted in principle**. It is
the **pragmatic layer that makes the architectural rules concrete enough for the
agents that build the code**: where an architectural golden rule states a
near-universal, cross-domain shape, a convention operationalizes it for one
domain. "Use Rust where it can be done cleanly," "every human surface is one
Flutter codebase" — each is a settled answer for its domain, not a fresh decision
re-litigated per project.

This register is **stature band 3** of the shared-knowledge body — below the
architectural golden rules ([`golden-rules/`](../golden-rules/)) and above the
frozen decisions ([`adr/`](../adr/)). The band, its marks, and its place in the
gradient are defined once, authoritatively, in
[`../ONTOLOGY.md`](../ONTOLOGY.md); this register consults that definition rather
than restating it, and holds the stratum's membership and its working norms.

## Rooted in principles

A convention relates to the principles by **citation**: it **cites the universals
beneath it** (`rooted-in`) as the ground its choice rests on. The convention
names the principles; it does not contain them, and it is not one of them — their
single home is
[`pentaxis93/principles`](https://github.com/pentaxis93/principles).

This is the same `rooted-in` relation the architectural golden rules carry, and
the distinction between it and the corpus's internal **projection** mechanism (a
universal's own domain face, authored and owned inside the corpus) is drawn
precisely in the [golden-rules register](../golden-rules/README.md#rooted-in-principles-not-a-projection-of-them).
A convention cites principles as roots; it never lives *among* them.

## The conventions

The conventions below are the stratum's current members. A convention may enter
as an **unfleshed seed** — its evocative capture held intact in the stratum's
tracker work — and is fleshed into its own durable form **one at a time**, on
the operator-pointed evidence for each. A convention's **Status** links to its
fleshed home once that fleshing lands.

| Convention | Rooted in | Domain | Status |
| --- | --- | --- | --- |
| **Rust wherever it can be done cleanly** — where a component can be written cleanly in Rust, Rust is the default, not a candidate; correctness made structural by the type system. | [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md) · [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md) · [Honest Signal](https://github.com/pentaxis93/principles/blob/main/principles/honest-signal.md) | Implementation | [fleshed](rust-where-clean.md) |
| **Flutter wherever there is a user interface** — every human-facing surface is one expressive, declarative Flutter codebase: the interface expressed once, coherent everywhere, maintained once. | [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) · [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md) · [Transmission](https://github.com/pentaxis93/principles/blob/main/principles/transmission.md) | User interface | seed |
| **Roadmap graph** — the work-unit graph is homed as nested roadmaps: each node is the single home of its immediate children, and a cross-branch dependency is homed at its nearest common ancestor — Single Home by partition. | [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) · [Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md) | Work tracking | [fleshed](roadmap-graph.md) |

## Register norms

- A convention **cites** its root principles (`rooted-in`); it never restates or
  relocates them. The universals' single home is
  [`pentaxis93/principles`](https://github.com/pentaxis93/principles).
- Membership is recorded in the table above. A convention earns a row when a
  master has settled it for a class of work spanning more than one pentaxis93
  project.
- A convention enters as a **seed** — its evocative capture preserved intact —
  and is **fleshed one at a time**, on the operator-pointed evidence for each. A
  seed's row gains a link to its fleshed home when that fleshing lands.
- Fleshing a convention is never flattening it: the rich capture is the seed of
  the fleshed form, not a cost to economize.
- The band above is the architectural golden rules
  ([`golden-rules/`](../golden-rules/)); a convention operationalizes those rules
  for its domain. The full stature gradient is in [`../ONTOLOGY.md`](../ONTOLOGY.md).
