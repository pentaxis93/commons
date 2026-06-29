# Architectural Layers Bounded by Contracts

**Stratum:** Golden Rules · [Register](README.md)
**Domain:** System architecture
**Rooted in:** [Contract-First](https://github.com/pentaxis93/principles/blob/main/compositions/contract-first.md) · [Evolvability](https://github.com/pentaxis93/principles/blob/main/principles/evolvability.md) · [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md)

> **The rule.** A layer depends only on the **contract** of what it uses — a
> declared, checkable surface — never on the implementation behind it. The
> contract is owned by the more stable side; the volatile side is a swappable
> adapter built to it. Dependencies therefore run toward the abstraction, never
> toward the detail — and an implementation can be replaced behind its contract
> without any dependent knowing.

## The rule, precisely

A layer's only knowledge of what it uses is the **contract** — the declared,
checkable surface of the seam between them: a schema, an interface, an operation
set. It holds no knowledge of the implementation behind that surface and names
nothing from it. Dependencies run in one direction only — toward the more stable
abstraction — so the contract is owned by the side that changes least, and the
volatile side is built to it. When control must flow the other way, the
dependency is **inverted, not reversed**: the stable side declares the surface
and the volatile side implements it, so the source-code dependency still points
at the abstraction even as the call points at the detail.

What crosses the boundary is only what the contract declares; each side's HOW —
how it satisfies the contract — stays its own. The implementation behind the
contract is therefore a **swappable adapter**: replace it with another that
meets the same surface and nothing across the boundary changes, because nothing
across the boundary ever depended on it. The contract is the single home of the
seam's truth — both sides consult it or derive from it, neither restates it —
and each side's conformance is decided *against the contract* as evidence, never
taken on the side's own report. The boundary is real only to the degree the
contract is declared, checkable, and the gate.

## Rooted in principles

This rule cites the universals beneath it; it does not contain them, and it is
not one of them.

- **[Contract-First](https://github.com/pentaxis93/principles/blob/main/compositions/contract-first.md)** — *declare the seam, build to it, verify
  against it.* This rule is that composition realized as layering: the contract
  is the declared seam between two layers, each layer is built to it, and each
  is verified against it. The composition's own constituents all hold across the
  layer boundary — **Sovereignty** (the boundary; each side's HOW its own),
  **Single Home** (the contract the one locus of the seam's truth), **Sequence**
  (the contract declared before either side is built to it), and **Verifiable
  Completion** (the contract the gate, not the side's report).
- **[Evolvability](https://github.com/pentaxis93/principles/blob/main/principles/evolvability.md)** — *build so the next change is cheap; debt does
  not flow forward.* The contract is the stable seam, and the volatile detail
  lives behind it as a swappable adapter — so the change most likely to come (a
  new provider, a new mechanism, a new methodology) is the cheap one. Depending
  on the implementation instead would send that change's cost forward into every
  dependent.
- **[Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md)** — *everything earns its place.* The contract carries
  only the WHAT that must cross the boundary, and nothing the seam does not
  demand. A contract that leaks the implementation's incidentals draws a wider
  boundary than the seam requires, and the surplus is unearned coupling.

## The invariant beneath

A golden rule earns its standing by instancing a structure deeper than itself —
a principle beneath, a master above. The structure this rule projects:

> A part depends only on the declared contract of what it uses, never on its
> implementation; the dependency runs toward the more stable abstraction, and
> the volatile detail is a replaceable adapter behind the contract.

Reduced to its shape:

```
   contract  (stable abstraction)
      ↑ depends-on
   adapter   (volatile detail)
```

— the arrow of dependency points always at the abstraction, never at the detail,
whichever way control happens to flow.

This structure is not a software convenience. It is the architectural form of
separating policy from detail at the point where policy has no knowledge of
detail, and it was independently arrived at across decades of software
architecture — Clean Architecture, Hexagonal / Ports-and-Adapters, Onion, BCE —
and, outside computation entirely, in every system built from interchangeable
parts behind a standard interface. That wholly different domains realize the
same structure is the evidence the structure is **objective** rather than a
local habit, which is what lets this rule stand as a golden rule and not merely
a preference.

## Domain and scope

The rule governs systems decomposable into layers of **differential stability**:
some parts are more abstract and change-resistant (policy), others are concrete
and volatile (mechanism), and the boundary between them can be **declared as a
checkable contract**. Where those conditions hold, dependency toward the
abstraction is the right shape; where a boundary cannot be made into a real
contract, "depend on the contract" has nothing to bind to and the rule does not
apply.

Scoped this way, the rule covers a single program's internal layers — a domain
core and its adapters — as fully as it covers a distributed system's service
boundaries or an **agent runtime's plugin seams**: a methodology behind a
manifest-and-schema contract, a forge provider behind an operation-set contract,
an agent runtime behind a configuration surface. The differential in stability
across a declarable boundary, not the deployment unit, is what the rule turns
on.

## What the rule requires

A contract is load-bearing only if it is **checkable and enforced**. A declared
surface that is never validated against — an interface no implementation is
checked to satisfy, a schema no instance is tested against — is a contract in
name only, and the boundary it claims to draw leaks. A lawful
layers-bounded-by-contracts system therefore carries **conformance checking at
the boundary**: each adapter is verified against the contract it claims to
implement, and a dependent receives only what the contract guarantees. This
requirement is not an addendum to the rule; it is the rule's Verifiable-Completion
half made explicit — the contract is the boundary only because it is the gate.

## Boundaries

- This rule is **not "state is the interface."** That components meet only in
  durable state (the sibling rule *State is the interface*) is about the
  *medium* actors coordinate through; this rule is about the *direction of
  dependency* across a layer boundary and what is owned on each side. A system
  holds both at once — state as the medium, contracts as the boundaries — and
  they answer different questions.
- A contract is a real boundary, but **not an impermeable one.** The rule's
  claim is that the *declared surface* is all a dependent knows of its
  dependency — not that the two sides share nothing causal. Two layers may still
  run in one process, on one clock, against shared resources; the rule asks that
  the *dependency* be on the contract, not that all coupling vanish.
- "More stable" is a **judgment, not a given.** Which side is the abstraction
  and which the detail is a design call about what is likely to change. The rule
  says depend toward stability; it does not hand you which side that is. A
  boundary drawn with the volatile side cast as the "contract" inverts the
  protection the rule exists to provide.

## Cross-domain evidence: convergent architecture and the interchangeable part

The invariant this rule projects was not invented; it was independently arrived
at across decades of software architecture, which is the strongest evidence it
is objective. Robert C. Martin's **Clean Architecture** states it as the
Dependency Rule — source-code dependencies point only inward, toward
higher-level policy, while the details (the database, the web) are kept on the
outside where they can do little harm — with the Dependency Inversion Principle
as the mechanism that makes a dependency oppose the flow of control. The same
structure is Alistair Cockburn's **Hexagonal Architecture (Ports and
Adapters)**, Jeffrey Palermo's **Onion Architecture**, and Ivar Jacobson's
**BCE** — each varying in detail, each reaching the same objective: separate
concerns into layers and depend in the direction of stability and abstraction.
Independent arrival at one structure, by people not copying one another, is what
distinguishes an objective invariant from a local convention.

Outside software the same structure is the **interchangeable part behind a
standard interface**: a wall socket is a contract and every appliance a swappable
adapter built to it; a lightbulb socket, a shipping container, a screw thread, a
network protocol — each is a declared surface that lets the thing behind it be
replaced without disturbing anything that depends on it. The standard is owned by
the stable side and the implementations are the volatile, replaceable side. This
is the rule's invariant in a domain with no source code at all: depend on the
declared interface, and the part behind it becomes free to change.

The convergence is cited as evidence the invariant is objective, never as the
rule's authority. "Architectural layers bounded by contracts" stands on its
principle roots — Contract-First, Evolvability, Parsimony — and on the
architectural reasoning above; the independent arrivals corroborate that the
structure recurs wherever parts of differing stability must compose. The rule is
the **faithful generalization** of that converged-upon structure into agentic
architecture, claiming no novelty: the same Dependency Rule, lifted from
object-oriented source-code dependencies to the layers of an agent system, where
the policy is the methodology and runtime and the details are the methodology
plugin, the forge provider, and the agent runtime — each a swappable adapter
behind its contract.

## Relations

- **sibling** — *State is the interface* ([fleshed](state-is-the-interface.md)):
  this rule names the *boundary* between layers (the contract); the state rule
  names the *medium* components meet through (durable state, not calls). Boundary
  and medium are distinct rules a system holds together.
- **sibling** — *Right Action* ([fleshed](right-action.md)): this rule bounds the
  layers; Right Action shapes the unit of work that runs across them — the
  contract is the surface, Right Action an idempotent act that reads it and
  satisfies it. Two rules, not one.
- **kin** — *Rust wherever it can be done cleanly* ([register](README.md)): in a
  Rust component the contract is a trait the compiler enforces — the type system
  makes the boundary structural, checked before the code runs, which is the
  *checkable-and-enforced* requirement met for free.
- **roots** — Contract-First, Evolvability, Parsimony (above).

## Sources

- Root principle and composition: [Contract-First](https://github.com/pentaxis93/principles/blob/main/compositions/contract-first.md), [Evolvability](https://github.com/pentaxis93/principles/blob/main/principles/evolvability.md), [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md) — `pentaxis93/principles`.
- Cross-domain evidence: Robert C. Martin, [*The Clean Architecture*](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) (the Dependency Rule and Dependency Inversion) and *Clean Architecture: A Craftsman's Guide to Software Structure and Design* (ch. 22); the convergent canon it names — Cockburn's Hexagonal / Ports-and-Adapters, Palermo's Onion, Jacobson's BCE.
- Realization: the rule is realized in the Tesserine runtime — `tesserine/runa` [`ARCHITECTURE.md`](https://github.com/tesserine/runa/blob/main/ARCHITECTURE.md) (the manifest-and-schema, forge-operation, artifact-production, and MCP contracts, each with its swappable adapters) — which this rule governs and which consults it rather than restating it.
- Founding capture: this stratum's seed for the rule (`pentaxis93/commons` #16).
