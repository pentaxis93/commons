# Flutter Wherever There Is a User Interface

**Stratum:** Conventions · [Register](README.md)
**Domain:** User interface
**Rooted in:** [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) · [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md) · [Transmission](https://github.com/pentaxis93/principles/blob/main/principles/transmission.md)

> **The convention.** Where the system meets a human through a **user
> interface**, build that interface in **Flutter** — one expressive,
> declarative codebase across every surface a person touches. The interface
> is expressed once and rendered natively everywhere: mobile, desktop, and
> web are one product, not three. Flutter earns this standing because a
> declarative UI is a pure function of state, which closes the surface into
> the same state-centric discipline that governs the engine — the screen
> becomes a projection of state, not a second place where truth lives.

## The rule, precisely

For user-interface work — any human-facing surface across the ecosystem —
Flutter is the standing answer, applied under one boundary.

- **Where there is a UI, it is one Flutter codebase.** A human-facing surface
  is expressed once in Flutter and rendered to each platform from that single
  expression, not rebuilt per platform and not weighed afresh against the
  alternatives each time. The decision is settled for the class; a project
  does not re-litigate it.

- **The *user interface* qualifier bounds the rule.** The convention governs
  the surface where a human interacts — not the engine, the runtime, the
  service, or the back end behind it. Those are implementation domains the
  rule leaves to their own standing answer ([Rust wherever it can be done
  cleanly](rust-where-clean.md)). The boundary is part of the convention, not
  an escape from it: the rule draws a clean seam between the human surface and
  the machinery beneath it, and naming which side a component sits on is the
  rule working, not failing.

- **The selection axis is one coherent product, not per-platform optimum.**
  The rule optimizes for an interface that is the same language wherever it is
  touched — learned once, maintained once, coherent across every surface — not
  for squeezing the last platform-specific affordance out of each target
  separately. That a single codebase yields to each platform rather than being
  hand-tuned per platform is the trade the convention makes deliberately, and
  is where the rule wants the cost to fall.

## Why Flutter earns the default

Two grounds support the rule. The first is what Flutter *is*; the second is
the established reasoning for the way this work is actually carried out.
Neither is asserted from the framework's reputation — the first is grounded in
the framework's documented model, the second in the reasoning recorded in
[`pentaxis93/eterne`](https://github.com/pentaxis93/eterne) (the unified-app
and sutra-browser specs, cited here rather than reproduced).

### One surface, expressed once

Flutter's model is an objective property of the framework, and each face of it
maps to a root principle:

- **One codebase is the interface's single home.** A declarative Flutter
  application is the one authoritative expression of the interface; each
  platform's rendering derives from that single expression rather than being a
  separately-maintained sibling. There is no per-platform copy to hold in sync
  by hand — the divergence a multi-codebase UI risks is removed structurally,
  because there is only one place the interface lives. This is
  [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md):
  the surface has exactly one home, and every platform consumes it.

- **The interface is paid for once, not N times.** Building a UI once and
  rendering it everywhere is disciplined completeness, not doing less — every
  surface a human touches is served, and nothing is carried N times for the N
  platforms it must reach. A per-platform UI pays the full cost of the same
  interface repeatedly; the convention removes that unearned multiplication.
  This is [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md):
  the shape is demanded by the need — reach every surface — without paying for
  the same expression more than once.

- **One language the user learns once.** A single coherent interface across
  every surface is one language a person learns once and carries everywhere,
  rather than a different dialect per platform that forces relearning at each
  door. The interface lands in the recipient's hands in a register they
  already hold, because it is the same register on every surface. This is
  [Transmission](https://github.com/pentaxis93/principles/blob/main/principles/transmission.md):
  the artifact fits the recipient, and a uniform surface across the ecosystem
  amortizes the cognitive cost instead of compounding it.

### Declarative UI closes the loop with state

The second ground is the established reason the convention exists at all, and
it is the link from this convention up to the architectural band. A declarative
UI is a pure function of state: the screen is computed from the current state
rather than mutated step by step toward it. That is the surface form of the
architectural rule [*state is the interface*](../golden-rules/state-is-the-interface.md) —
the screen becomes a projection of state, and the same state-centric discipline
that governs the engine governs the surface. The interface stops being a second
place where truth is held and maintained, and becomes a view of the one state
the system already owns.

The lived evidence is recorded in the eterne material — a unified personal
operating system specified as a single Flutter application across its layers,
with its data modeled as immutable state and its screens derived from that
state ("plain Flutter, obvious patterns," "immutable data, no edit mode").
The direction the convention encodes is one product expressed once, its
interface a function of the state beneath it, coherent on every surface a human
reaches.

The full established reasoning lives in the eterne vault and is the
convention's evidence home; this document grounds its claims in that material
and in the framework's documented model, and restates neither wholesale.

## Boundaries

- The convention governs *the technology of the human-facing surface*. It does
  not dictate how a given interface is designed once Flutter is chosen — screen
  composition, state-management library, navigation, and widget structure are
  the implementer's, bounded by the architectural rules this convention
  operationalizes.
- The *user interface* qualifier is a stated boundary, not a loophole: the rule
  is the default for human-facing surfaces, and it leaves the engine, runtime,
  and service domains to their own standing answer. A component built in another
  technology because it is not a user interface is consistent with the
  convention, not an exception to it.
- The convention is a standing answer for a class of work spanning more than one
  pentaxis93 project; it is not a per-project decision and not a universal law
  of all software.

## Relations

- **roots** — [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md),
  [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md),
  [Transmission](https://github.com/pentaxis93/principles/blob/main/principles/transmission.md)
  (`rooted-in`, above): one UI codebase as the interface's single home, the
  interface paid for once rather than per platform, and one coherent language
  the user learns once are the universals the framework realizes.
- **operationalizes** — the architectural golden rules
  ([`golden-rules/`](../golden-rules/)): a convention makes the architectural
  band concrete for one domain, and this convention operationalizes
  [*State is the interface*](../golden-rules/state-is-the-interface.md) for the
  user-interface domain by choosing a framework in which the screen is a
  declarative projection of state rather than a separately-mutated surface.
- **kin** — [Rust wherever it can be done cleanly](rust-where-clean.md): the
  two conventions partition the build by the seam between the human surface and
  the machinery beneath it. Flutter is the standing answer where there is a
  user interface; Rust is the standing answer for the implementation work
  behind it. Each names its own side, and the boundary one draws is the domain
  the other holds.

## Sources

- Established reasoning: [`pentaxis93/eterne`](https://github.com/pentaxis93/eterne)
  — the unified-app spec (`spec-unified-app.md`) and the sutra-browser MVP spec
  (`spec-sutra-browser.md`): one Flutter application across the layers, immutable
  state, and the screen derived from that state, mined as this convention's
  evidence home.
- Founding seed and freshen: `pentaxis93/commons` #18.
- Fleshed-convention shape: [`conventions/rust-where-clean.md`](rust-where-clean.md),
  the register's sibling implementation-domain convention, and
  [`conventions/roadmap-graph.md`](roadmap-graph.md), the register's first
  fleshed convention.
