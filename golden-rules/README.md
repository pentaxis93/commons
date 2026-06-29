# Golden-Rules Register

Domain-specific architectural rules for the pentaxis93 projects. This register
is the index; each rule is authoritative for its own content once fleshed.

A **golden rule** is a domain-specific architectural choice, **rooted in
principle** and **master-curated**: a decision a domain master makes for a
whole class of work, having paid the price of the alternatives. "Use Rust where
it can be done cleanly," "every human surface is one Flutter codebase,"
"components meet only in state" — each is a standing answer for its domain, not
a fresh decision re-litigated per project.

This is the bar for living here: a rule belongs when it governs more than one
pentaxis93 project and a master has settled it. The rules govern with-claude
and oracy as much as the Tesserine ecosystem, which is why their home is this
repository — the pentaxis93 base — and not any one project's authority.

## Rooted in principles, not a projection of them

A golden rule and a principle are different things, and the difference is the
reason this register exists separately from
[`pentaxis93/principles`](https://github.com/pentaxis93/principles).

- A **principle** is **domain-neutral** — the invariant that holds across any
  domain (Sovereignty, Parsimony, Verifiable Completion). Its home is the
  principles corpus.
- A **golden rule** is **domain-specific** — a master's choice for a class of
  work (a language, an architectural shape, a unit of work). Its home is here.

A golden rule relates to the principles by **citation**: it **cites the
universals beneath it** (`rooted-in`) as the ground its choice rests on. The
rule names the principles; it does not contain them, and it is not one of them.

This is **not** the corpus's **projection** mechanism. The corpus already has a
way to express a universal in a domain form — a *projection* (Grounding's
"ground to needs, not to code," Sovereignty's "declarative framing"). A
projection is **a face of a universal, authored and owned inside the corpus**;
it points *down* from the universal to its own domain instance.

The two "domain form of a principle" mechanisms are deliberately distinct, so
neither duplicates the other's role ([Single
Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md)):

| | Projection | Golden rule (`rooted-in`) |
| --- | --- | --- |
| **Home** | inside `pentaxis93/principles` | here, in `pentaxis93/commons` |
| **Owns** | a universal's own domain face | a master's domain-specific choice |
| **Direction** | universal → its domain instance | rule → the universals it cites |
| **Authored by** | the corpus, as part of the universal | a domain master who chose it |

A golden rule cites principles as roots; it never lives *among* them, and the
projection mechanism stays internal to the corpus.

## The rules

The five rules below are the stratum's founding members. Each enters as an
**unfleshed seed** — its evocative capture held intact in the stratum's tracker
work — and is fleshed into its own durable form **one at a time**, in the
sequence the framing epic carries (#14). The seed is captured richly first and
flattened never; fleshing is a later, sequenced move, not this register's job. A
rule's **Status** links to its fleshed home once that fleshing lands.

| Rule | Rooted in | Domain | Status |
| --- | --- | --- | --- |
| **State is the interface** — components meet only through durable, legible state: read it, write it; the state is the single source of truth and the only thing between them. | [Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md) · [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md) · [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) | System architecture | [fleshed](state-is-the-interface.md) |
| **Architectural layers bounded by contracts** — each layer depends on the *contract* of the layer it uses, never its implementation; implementations are swappable adapters behind the boundary. | [Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md) · [Evolvability](https://github.com/pentaxis93/principles/blob/main/principles/evolvability.md) · [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md) | System architecture | seed |
| **Rust wherever it can be done cleanly** — where a component can be written cleanly in Rust, Rust is the default, not a candidate; correctness made structural by the type system. | [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md) · [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md) · [Honest Signal](https://github.com/pentaxis93/principles/blob/main/principles/honest-signal.md) | Implementation | seed |
| **Flutter wherever there is a user interface** — every human-facing surface is one expressive, declarative Flutter codebase: the interface expressed once, coherent everywhere, maintained once. | [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) · [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md) · [Transmission](https://github.com/pentaxis93/principles/blob/main/principles/transmission.md) | User interface | seed |
| **One idempotent operation that infers its work from state** — the unit of work is a single idempotent move that reads the state, infers what it needs, and does exactly that; run again, it converges rather than accumulates. *(exigence-driven work)* | [Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md) · [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md) · [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md) · [Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md) | The shape of work | seed |

## Conventions

- A golden rule **cites** its root principles (`rooted-in`); it never restates
  or relocates them. The universals' single home is
  [`pentaxis93/principles`](https://github.com/pentaxis93/principles).
- Membership is recorded in the table above. A rule earns a row when a master
  has settled it for a class of work spanning more than one pentaxis93 project.
- A rule enters as a **seed** — its evocative capture preserved intact — and is
  **fleshed one at a time**, in the sequence the framing epic carries (#14). A
  seed's row gains a link to its fleshed home when that fleshing lands.
- Fleshing a rule is never flattening it: the rich capture is the seed of the
  fleshed form, not a cost to economize.
