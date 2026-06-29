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

State is the interface **of authority**. A component carries nothing of its own
across the boundary — no private authority, no plan held in reserve; it has only
the present configuration it can read and the operation it can apply to what it
finds there. Coordination happens because each operation changes the
configuration that later operations read: actors never meet one another — they
meet only in the trace each leaves. None hosts another; none need be running for
another to proceed; the coordination truth is written down, now, and is
therefore inspectable at every instant.

What a component brings is not content but **capacity**. The **response
functions** — the code, invariants, permissions, and domain constraints it runs
— are its trained ability to read what is present and answer it; the work to be
done, the truth it answers to, and the continuity it hands on are not held
within the component but stand in the shared field, which it meets reading what
is there and leaves having written what now is. "No held plan" is not "no
structure": structure is in the response function — *how* to read and act —
while *what* to act on is in the state. Authority is in the medium; capacity is
in the actor; nothing of substance passes between them but the reading and the
writing.

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

> Authority lives in the present medium all legitimate actors can perceive and
> change; each actor meets that medium empty — carrying no work and no plan of
> its own — and acts as a bounded local response to the pressure present there;
> continuity is the trace left in the medium, never anything an actor holds.

Reduced to its loop:

```
present configuration → perceived pressure → local response → changed configuration
```

— no actor persists inside the loop to carry the thread; the configuration carries it.

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
shape: the actor meets the present empty — carrying no plan and no self to
assert — and what is present comes forth of its own accord to be answered;
action is that answer, and it leaves a trace that conditions what comes next.
Its precise name is **nondual responsive action**. Daoist *wu-wei* names the act
— effective response without forcing intention — and *ziran*, the self-so, names
its ground: the world unfolding of itself, the field the empty actor answers
rather than authors. Buddhist *not-self / dependent arising* names the
no-controller ontology — action as a conditioned event, not the act of an
enduring agent. Chan/Zen *no-mind*, and Dōgen's *genjō* — the present
manifesting here and now — name the integrated shape: the actor so empty that
the present meets it without obstruction, and the work comes forth from the
field rather than from a self carried into it. The same load-bearing relations
hold across the mapping: authority in what is present rather than a stored plan;
the actor empty of its own continuity; coherent action without a sovereign
executor; continuity carried by the trace rather than anything an actor holds;
and corruption taking the same form on both sides — a private continuity carried
forward (a stale controller, a clung plan, a self asserted over what is)
overriding the present.

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
