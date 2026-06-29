# Ontology

The shared-knowledge body that governs the pentaxis93 projects and the Tesserine
ecosystem is organized by **two orthogonal hierarchies**. This document is the
single authoritative statement of that organization: it names both hierarchies,
gives the stature gradient its bands and their homes, and states how the two
compose.

It sits one level above
[`pentaxis93/principles`'s `ONTOLOGY.md`](https://github.com/pentaxis93/principles/blob/main/ONTOLOGY.md).
That document is the form contract for the principles corpus's *internal*
structure — the relationship taxonomy among the universals, the document schema,
the four-movement topology. This document is the form contract for the
*cross-stratum* structure of the whole body: it places the corpus as one band
and points at that document for the band's interior, rather than restating it.

## The two hierarchies

A claim in the shared-knowledge body has a coordinate on two independent axes.

- **Stature** — *how universal the claim is, and how it came to be known.* A
  descending gradient from a discovered domain-neutral invariant to a concrete
  built artifact: **universal principle → architectural golden rule → convention
  → decision → concrete asset.** This is the gradient the repository layout
  leaves implicit; this document makes it explicit.
- **Authority** — *whom the claim binds, and who may override it.* An
  inheritance chain from the universal base outward: **universal → pentaxis93
  base → ecosystem → project.** This is carried by the repository inheritance
  chain; this document references it and states how it composes with stature.

The axes are orthogonal. Stature says *what kind of claim* this is; authority
says *whose claim it is and who may change it.* A single asset has a position on
both — a golden rule (a stature band) homed at the pentaxis93 base (an authority
tier).

## The stature gradient

Five bands, most universal first. Each band is fixed by three marks — its
**universality**, its **epistemic origin** (discovered → curated → decided →
built), and its **mutability register** (how, and how readily, it changes) — and
each has one home.

| Band | Universality | Origin | Mutability | Home |
|---|---|---|---|---|
| **Universal principle** | domain-neutral invariant | discovered | evolves only as the corpus evolves — rare, high-deliberation | [`pentaxis93/principles`](https://github.com/pentaxis93/principles) |
| **Architectural golden rule** | near-universal, cross-domain | master-curated | re-curated when a master revises the standing answer | [`golden-rules/`](golden-rules/) |
| **Convention** | domain-specific (a language, a framework, a practice) | master-curated | re-curated per domain | the conventions register, a sibling register to `golden-rules/` |
| **Decision / ADR** | a specific, singular choice | decided | frozen — superseded, never edited | [`adr/`](adr/) |
| **Concrete asset** | a concrete instance | built | revised freely as the artifact improves | the repository's asset files |

A lower band **rests on the bands above it by reference, never by restatement** —
the defining discipline of the whole body
([Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md)):

- A **universal principle** is a discovered, domain-neutral invariant, owned in
  the corpus and *consulted* everywhere — contained nowhere else. Its members are
  the universals and the named compositions;
  [`principles/ONTOLOGY.md`](https://github.com/pentaxis93/principles/blob/main/ONTOLOGY.md)
  details their interior structure.
- An **architectural golden rule** is a master's near-universal, cross-domain
  choice for a class of work, **`rooted-in`** the universals it cites — a
  citation upward, not a projection downward (the
  [register](golden-rules/README.md) draws that distinction precisely). Members:
  *State is the interface*, *Architectural layers bounded by contracts*, *Right
  Action*.
- A **convention** is a master's domain-specific choice — the pragmatic layer
  that makes the architectural rules concrete enough for the agents that build
  the code. It is **`rooted-in`** principle and operationalizes the architectural
  rules for one domain. Members: *Rust wherever it can be done cleanly*, *Flutter
  wherever there is a user interface*, *the multi-dimensional contract*.
- A **decision / ADR** is a single past choice carrying its rationale,
  **`traces-to`** the principles it serves, and may **`instantiate`** a golden
  rule. It is frozen: a superseded decision is tombstoned, not rewritten. Member:
  ADR-0001 (the repository merge-and-history policy).
- A **concrete asset** is a reusable artifact — a baseline, a script, a
  discipline document — that **instantiates** the bands above. Members: the FCOS
  host-setup baseline ([`install-fcos.sh`](install-fcos.sh) +
  [`fcos-host-setup/`](fcos-host-setup/)), the
  [deployment-documentation discipline](DEPLOYMENT-DOCUMENTATION-DISCIPLINE.md).

The band is legible from where an asset lives: a file under `golden-rules/` is an
architectural rule, one under `adr/` is a decision, the corpus is the principle
band. Placing a new claim is choosing its band by its marks — *discovered and
domain-neutral? a master's cross-domain choice? a domain-specific convention? a
frozen decision? a built artifact?* — and the band names its one home and one
procedure.

## The authority gradient

The inheritance chain runs from the universal base outward, each tier a **config
overlay** on the one beneath:

**[`pentaxis93/principles`](https://github.com/pentaxis93/principles) →
[`pentaxis93/commons`](https://github.com/pentaxis93/commons) (the pentaxis93
base) → [`tesserine/commons`](https://github.com/tesserine/commons) (the
ecosystem) → individual projects.**

This chain is **declared and wired**, and this document points at the declaration
rather than restating it:
[`tesserine/commons`'s `## Foundation` section](https://github.com/tesserine/commons)
names its base and the overlay rule, ADR-0001 states its own base-hood, and the
[golden-rules register](golden-rules/README.md) names the pentaxis93 base as the
rules' home. The principles corpus keeps a single home consumed across the
organization boundary — it is not re-homed per tier.

## How the two compose

At each authority tier, a stature band is **Added**, **Overridden**, or
**Consumed** — the config-overlay rule, applied per band:

- **Consume** — use a base member unchanged. Most members are consumed: the
  ecosystem consults the principles and the pentaxis93 golden rules as given.
  (A concrete consume: `tesserine/commons` inherits pentaxis93's ADR-0001 in
  place of carrying its own merge-policy ADR.)
- **Add** — contribute a new member at this tier: the ecosystem's own decisions
  and conventions, layered on top of the base.
- **Override** — replace a base member where this tier genuinely must differ.
  Reserved for where a tier cannot consume the base.

The one band that does not override is the **universal principle**: a tier
consumes it, or it is not universal. Overriding a domain-neutral invariant would
re-entangle it with a domain, dissolving the independent consumability that gives
the corpus its single home across the organization boundary. That invariant is
why the principles corpus stays a separate, consumed repository rather than
merging into any base.

## Maintaining this ontology

This is a **living, curation-maintained statement**, not a frozen record: it is
revised in place as the body's structure changes, and it carries no
decision-record shape. A new band, a new member, or a reclassification lands
here, and the asset it concerns moves to the home this document names. Changes to
the *ontology itself* are the recursive spiral acting on this asset; friction
with it is a change-vector on `pentaxis93/commons`.
