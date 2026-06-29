# State Is the Interface

**Stratum:** Golden Rules · [Register](README.md)
**Domain:** System architecture
**Rooted in:** [Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md) · [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md) · [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md)

> **The rule.** Components meet only through durable, legible **state**. Each
> component reads the state, infers from it what is now needed, and writes the
> state. The state is the single source of truth and the only thing between
> them — no running controller, no hidden queue, no direct pairwise dependency.
> Continuity is carried by the trace.

## The rule, precisely

State is the interface **of authority**. A component holds no authority beyond
the present configuration it can read and the operation it can apply to it.
Coordination happens because each operation changes the state that later
operations read: actors never meet one another — they meet only in the trace
each leaves. None hosts another; none need be running for another to proceed;
the coordination truth is written down, now, and is therefore inspectable at
every instant.

The state is the interface of authority; the **response functions** — the code,
invariants, permissions, and domain constraints a component runs — are the
trained capacities that read the state and transform it. "No held plan" is not
"no structure": the plan does not live in a running coordinator, but the
response function does the work of reading the present pressure and converging
on it. Authority lives in the medium; capability lives in the response function;
neither lives in a private, running executive.

## Rooted in principles

This rule cites the universals beneath it; it does not contain them, and it is
not one of them.

- **[Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md)** — *every inference earns its chain.* State is the
  evidence: nothing is true until it is written into the state, where its path
  back to ground is explicit and auditable. A claim that lives only in an
  actor's private intention has no chain.
- **[Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md)** — *completion is an observable
  state.* Work is proven by what the state shows, never asserted by the worker;
  the evidence lives in the state, and the evidence comes first.
- **[Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md)** — *everything shared has exactly one home.* The
  state is the one authoritative locus the shared truth lives in; every actor
  consults it rather than holding a divergent copy.

## The invariant beneath

A golden rule earns its standing by instancing a structure deeper than itself —
a principle beneath, a master above. The structure this rule projects:

> Authority lives in the medium all legitimate actors can perceive and change;
> action is a bounded local response to that medium's present pressure;
> coordination emerges through the trace left in the medium.

Reduced to its loop:

```
present configuration → perceived pressure → local response → changed configuration
```

— with no persistent executive actor required inside the loop.

This structure is not a software convenience. It appears independently in
stigmergic coordination (an action's trace in a medium stimulates the next
action, and tasks execute in order without a planner), in tuple-space and
blackboard coordination (actors read and write a shared field rather than
coupling directly), and — outside computation entirely — in the contemplative
shape described below. That a wholly different domain realizes the same
structure is the evidence the structure is **objective** rather than a local
habit, which is what lets this rule stand as a golden rule and not merely a
preference.

## Domain and scope

The rule governs systems where its load-bearing conditions hold: a **durable,
inspectable, shared state** can serve as the coordination medium, and actors
apply **bounded, convergent response functions** to it. Where those conditions
hold, this is the right shape; where they do not, "answer the present state"
degrades into nondeterminism rather than architecture.

Scoped this way, the rule covers single-actor-across-time resumability — the
next instance reads the state the last one left and continues, no actor needing
to have stayed running — as fully as it covers multi-actor coordination. The
medium, not the number of actors, is what the rule turns on.

## What the rule requires

Not every state-pressure is valid pressure. A bug, a panic, a malformed
configuration all present pressure; the rule does not license answering all of
it. A lawful state-is-interface system therefore carries **bounded response
functions, invariant checks, authorization, and error semantics** at the
boundary — without them, state pressure amplifies corruption rather than
converging it. This requirement is not an addendum to the rule; it is the rule's
own response-function half made explicit: the trained capacity that reads the
state is also what decides which pressure is worth answering.

## Boundaries

- This rule is **not idempotence.** That an operation reads state, infers its
  work, and converges on rerun is the sibling rule *One idempotent operation
  that infers its work from state* (the shape of the operation); this rule
  governs *that components meet only in state* (the medium between them). The
  medium and the act on it are distinct.
- "Legible" and "inspectable" are real but **not absolute.** The rule's claim is
  that the *coordination truth* is written down — not that all of a component's
  behavior is. A durable store can be wholly inspectable; the larger causal
  field a system sits in cannot. The rule asks that authority be inspectable,
  not that everything be.

## Cross-domain evidence: nondual responsive action

The invariant this rule projects is independently carried by a contemplative
shape: action that arises from present conditions, leaves a trace, and requires
no separate executive self. Its precise name is **nondual responsive action** —
Daoist *wu-wei / ziran* names the action-mode (effective action without forcing
intention), Buddhist *not-self / dependent arising* names the no-controller
ontology (action as a conditioned event, not the act of an enduring agent), and
Chan/Zen *no-mind* is the integrated shorthand. The same load-bearing relations
hold across the mapping: authority in present conditions rather than a stored
plan; coherent action without a sovereign executor; continuity carried by the
trace/stream rather than an actor-owned plan; and corruption taking the same
form on both sides — a private continuity (a stale controller; a clung plan)
overriding present conditions.

This congruence is **load-bearing but not load-sufficient.** It supports the
rule as one cross-domain expression of a real invariant; it is not an identity.
Three relations do not transfer, and each marks a boundary already drawn above:
machine inspectability has no contemplative correlate (a causal field is not a
database), mathematical idempotence is only rhymed by non-clinging (not exact
re-execution), and present pressure alone is insufficient on both sides — which
is exactly why the rule requires bounded response functions and validity checks.

The congruence is cited as evidence the invariant is objective, never as the
rule's authority. "State is the interface" stands on its principle roots and its
architectural reasoning; the contemplative shape corroborates that the structure
recurs across domains. It is **not** the claim "state is the interface because
Zen says action arises from the present" — that would be a vocabulary
resemblance, not a grounded rule.

The full structure-preserving analysis — the bidirectional mapping, the
congruence and unmapped zones, and the prediction tests against canonical
sources — has its home in the eterne research note cited below; this rule
consults it rather than restating it.

## Relations

- **sibling** — *Architectural layers bounded by contracts* ([register](README.md)):
  contracts name the boundary; this rule names what crosses it — durable state,
  not calls.
- **sibling** — *One idempotent operation that infers its work from state*
  ([register](README.md)): state-as-interface is the medium actors meet in; the
  idempotent operation is the single act that reads that medium and converges.
  The medium and the act are two rules, not one.
- **roots** — Traceability, Verifiable Completion, Single Home (above).

## Sources

- Root principles: [Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md), [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md), [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) — `pentaxis93/principles`.
- Cross-domain evidence: the contemplative-isomorphism analysis — `pentaxis93/eterne` `vault/archives/intelligence/research/research-2026-06-29-state-interface-contemplative-isomorphism.md` (verdict: real but partial; load-bearing not load-sufficient) — itself sourcing Heylighen on stigmergy, the Stanford Encyclopedia of Philosophy on Japanese Zen, Indian Buddhist mind, and Daoism, the Dao De Jing, and the Kubernetes / Kubebuilder reconciliation docs.
- Founding capture: this stratum's seed for the rule (`pentaxis93/commons` #15).
