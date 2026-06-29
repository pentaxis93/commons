# Rust Wherever It Can Be Done Cleanly

**Stratum:** Conventions · [Register](README.md)
**Domain:** Implementation
**Rooted in:** [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md) · [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md) · [Honest Signal](https://github.com/pentaxis93/principles/blob/main/principles/honest-signal.md)

> **The convention.** Where a component can be written cleanly in **Rust**,
> Rust is the default — not a candidate. The qualifier is load-bearing:
> *cleanly*, not against the grain. Rust earns this standing because it moves
> correctness from the programmer's vigilance into the type system, and because
> the constraints it enforces are exactly the kind agentic development thrives
> within — at each point in the code, the space of valid next moves is narrowed
> to the ones the compiler will accept.

## The rule, precisely

For implementation work — engines, runtimes, back ends, command-line tools,
anything where correctness and performance carry weight — Rust is the standing
answer, applied under one boundary.

- **Where Rust fits, it is the default.** A component that can be expressed in
  Rust without fighting the language is written in Rust, not weighed afresh
  against the alternatives each time. The decision is settled for the class; a
  project does not re-litigate it.

- **The *cleanly* qualifier bounds the rule.** Rust is the default where it can
  be done cleanly — not Rust-everywhere. Where a component would have to be
  written against the grain of the language, the rule does not force it. The
  boundary is part of the convention, not an escape from it: a domain where Rust
  is the wrong tool is a domain the rule leaves open, and naming that honestly is
  the rule working, not failing.

- **The selection axis is collaboration quality, not author comfort.** The rule
  optimizes for the quality of what the human–agent collaboration produces, not
  for how easy the language is for any one participant to learn. That Rust is
  demanding is granted and is not a reason to choose against it; the demand falls
  on the compiler's checking, which is where the rule wants it.

## Why Rust earns the default

Two grounds support the rule. The first is what Rust *is*; the second is what
Rust does for the way this work is actually carried out. Neither is asserted from
the language's reputation — the first is grounded in the language's documented
guarantees, the second in the established reasoning recorded in
[`pentaxis93/eterne`](https://github.com/pentaxis93/eterne) (the Rust
voice-transcripts, mined here and cited rather than reproduced).

### Correctness made structural

Rust's guarantees are objective properties of the language, and each maps to a
root principle:

- **Invalid states are made unrepresentable.** The type system and ownership
  model let a design encode its constraints so that whole classes of failure —
  memory unsafety, data races, the unhandled null, the state that should not
  exist — are rejected *before the program runs*. If it compiles, those failures
  are already impossible. Correctness becomes structural rather than vigilant:
  the discipline lives in the types, not in the programmer's sustained
  attention. This is [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md)
  made constitutive of the artifact — a compiling build is mechanical evidence
  that a declared class of error is absent, not a confidence level.

- **The compiler repairs the class at the source.** A whole category of defect
  is caught at the point of writing, at the boundary that creates it, rather
  than surfacing later at runtime far from its cause. The fix lands where the
  error originates. This is [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md):
  the class is eliminated at the emitter, not patched where it would otherwise
  be observed.

- **The type is the truth.** A value's type states honestly what it is and what
  may be done with it; absence and error are explicit in the type (`Option`,
  `Result`) rather than latent and discoverable only by failure. A surface
  cannot quietly claim a capability its type does not bear. This is
  [Honest Signal](https://github.com/pentaxis93/principles/blob/main/principles/honest-signal.md):
  the surface tells the truth about itself, enforced by the language.

Integrated testing and a coherent packaging and command model belong to the same
ground: testing sits inside the code rather than bolted alongside it, and a tool
packaged as a known command is trustworthy and reachable without navigating to a
directory or remembering an invocation — the behavior is where the name says it
is. Performance follows without a garbage collector's runtime tax.

### Constraint is what agentic development thrives within

The second ground is the established reason the convention exists at all. Agentic
work does its best within clear constraints, and Rust supplies them: it narrows
the space of valid choices at each point in the code. A complex, open-ended
reasoning problem becomes tractable for an agent when it is reduced to a bounded
decision — choosing among the few shapes the types and the borrow checker will
accept, rather than reasoning freely over an unbounded space. The same move that
turns a subtle problem into a categorization problem — picking which of a small
set of categories an input belongs to — is the move Rust applies continuously to
the act of writing code.

The standing objective this serves is lowering the coefficient of agentic
friction: keeping the collaboration focused on producing working artifacts. The
lived evidence is recorded in the eterne material — a personal-information-manager
service built as an MCP server in Rust came out clean and crisp, an excellent
build experience, and a later project's planning took time but, once construction
in Rust began, the system built it directly. The direction the convention encodes
is more structure, more constraint, more precision, with the agents given freedom
to solve problems creatively *within clearly defined spaces*.

The full established reasoning lives in the eterne vault and is the convention's
evidence home; this document grounds its claims in that material and in the
language's documented guarantees, and restates neither wholesale.

## Boundaries

- The convention governs *language selection for implementation work*. It does
  not dictate how a component is designed once Rust is chosen — architecture,
  module shape, error strategy, and crate choices are the implementer's, bounded
  by the architectural rules this convention operationalizes.
- The *cleanly* qualifier is a stated boundary, not a loophole: Rust is the
  default for components it fits, and the rule leaves open the domains where it
  does not. A component written in another language because Rust would be
  against the grain is consistent with the convention, not an exception to it.
- The convention is a standing answer for a class of work spanning more than one
  pentaxis93 project; it is not a per-project decision and not a universal law
  of all software.

## Relations

- **roots** — [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md),
  [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md),
  [Honest Signal](https://github.com/pentaxis93/principles/blob/main/principles/honest-signal.md)
  (`rooted-in`, above): correctness made structural and verifiable, the class
  repaired at the source by the compiler, and the type as an honest surface are
  the universals the language realizes.
- **operationalizes** — the architectural golden rules
  ([`golden-rules/`](../golden-rules/)): a convention makes the architectural
  band concrete for one domain, and this convention operationalizes the
  band for implementation by choosing a language in which correctness-by-construction
  — the substance beneath [*State is the interface*](../golden-rules/state-is-the-interface.md)
  and [*Architectural layers bounded by contracts*](../golden-rules/architectural-layers-bounded-by-contracts.md)
  — is enforced by the compiler rather than left to discipline.
- **kin** — [Flutter wherever there is a user interface](flutter-where-ui.md): the
  two conventions partition the build by the seam between the human surface and
  the machinery beneath it. Rust is the standing answer for the implementation
  work; Flutter is the standing answer where there is a user interface. Each
  names its own side, and the boundary one draws is the domain the other holds.

## Sources

- Established reasoning: [`pentaxis93/eterne`](https://github.com/pentaxis93/eterne)
  — the Rust voice-transcripts (the agentic-constraint hypothesis, the
  friction-coefficient objective, and the clean-and-crisp build experience),
  mined as this convention's evidence home.
- Founding seed and freshen: `pentaxis93/commons` #17.
- Fleshed-convention shape: [`conventions/roadmap-graph.md`](roadmap-graph.md),
  the register's first fleshed convention.
