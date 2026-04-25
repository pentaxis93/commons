# The Cognitive State Machine — Conceptual Foundation (Draft)

**Status:** Draft / exploratory. Aide-mémoire and seed for subsequent
reckoning sessions, not committed project direction.

**Origin:** Emerged from reckoning session, April 24, 2026, between Robbie
and Claude. The session began as a discussion of the use cases for a
strongly-typed cognitive state machine and converged on the recognition
that Tesserine already implements the substrate of one — and that the
trajectory from current state to full expression is now legible in
type-theoretic terms. A second reckoning later that day surfaced a
threshold framing in the trajectory; a third sharpened that threshold
to its current form. The framing is held as approach rather than
arrival — see open question #7.

**Eventual home (proposed):** tesserine/commons, as a foundational
concept document. Specific commitments derive from it as ADRs.

**Status before formalization:** Pre-work required (see final section).
The conceptual basis below is sharp enough to capture; it is not yet
sharp enough to commit the project to.

---

## The Basis

The cognitive state of an agent is carried by its artifacts. An
artifact is an idea-described-in-text. The artifact **is** the
cognitive state — there is no separate "state" floating alongside the
artifact that needs to be made type-shaped. The artifact's type
classifies the kind of cognitive content it carries.

A specific Hypothesis is to the type Hypothesis exactly what the value
`42` is to the type Integer. The type tells you what kind of thing the
artifact is; the artifact is a specific inhabitant of that type.

This collapses a confusion that obscured the structure of what
Tesserine has built. The system already implements a typed cognitive
state machine in the literal mathematical sense. The typing is not
aspirational; the typing **is** what makes protocol selection coherent.

## Protocols as Morphisms

A protocol is a typed transformation between artifact types. Examples:

- `Survey: Input → Survey`
- `Decompose: Survey → Decomposition`
- `Validate: (Hypothesis × Evidence) → ValidatedHypothesis | RefutedHypothesis`

The protocol's signature is its type. Inhabiting the morphism — performing
the transformation — produces the output artifact, which witnesses that
the morphism was performed.

In category-theory terms, Tesserine forms a small category:

- **Objects:** artifact types (Hypothesis, Evidence, Plan,
  Decomposition, etc.)
- **Morphisms:** protocols
- **Composition:** sequencing of protocols, with the dependency graph
  defining valid orderings
- **Identity:** the trivial no-op (probably needs no explicit
  existence)

This is a category in the precise sense. The categorial structure
already exists in Tesserine; what was missing was the vocabulary to
name it.

## Composition Primitives

The artifact type system supports — or could support, with
enrichment — the standard algebraic operations on types. Each operation
expresses a different way artifacts can carry cognitive structure.

### Subtyping (refinement)

`ValidatedHypothesis` is a subtype of `Hypothesis`: every validated
hypothesis is a hypothesis, plus carries validation evidence.
`RefutedHypothesis` is similar, with refutation evidence.

Subtyping enables polymorphism over cognitive states. A protocol like
`Cite: Hypothesis → Citation` accepts any Hypothesis. A protocol like
`Publish: ValidatedHypothesis → Publication` accepts only validated
ones. The cognitive constraint becomes a type constraint enforced by
the runtime.

Subtyping is also how artifacts become **witnesses**. A
`ValidatedHypothesis` is not merely "a hypothesis with a `validated:
true` field." It is a value that *only the Validate protocol can
construct*. Its existence proves validation occurred. The artifact
becomes proof; downstream consumers do not audit the producer.

### Products

Artifacts that combine. `(Hypothesis × Evidence)` is a pair type
carrying both. The Validate protocol operates on this product.
Composition of artifacts into compound artifacts is a product
operation.

### Sums

Artifacts that alternate. `(ValidatedHypothesis | RefutedHypothesis)`
is a sum type — the disjoint union of two possibilities, with the type
indicating which path was taken. Outcome-bearing protocols return sums.

### Recursion

Artifacts that contain themselves. A Decomposition whose subgoals are
themselves Decompositions. Tree-structured cognitive content has this
shape.

### Parameterization

Artifacts that generalize across domains. `Hypothesis[MedicalDomain]`
vs. `Hypothesis[SoftwareBugDomain]`. Same cognitive structure, different
subject matter. Domain-portability becomes a type-level operation.

### Sufficiency

These five operations (subtyping/refinement, products, sums, recursion,
parameterization) are sufficient to express any algebraic data type.
Tesserine's artifact type system today does not speak this vocabulary
explicitly. The Layer 2 work below is, in part, making it speak this
vocabulary.

## Methodology as Signature

A methodology in Tesserine declares what artifact types exist, what
protocols exist with their type signatures, and what sequencing
constraints apply. In algebraic terms, this is a **signature**: a set
of operations with their arities. The work of running a methodology
fills in the operations with cognitive content; the methodology defines
the shape.

Two methodologies with the same signature are *interface-equivalent*.
Two methodologies whose protocols satisfy the same equations are
*algebraically equivalent*. This is the basis on which homomorphisms
between methodologies become well-defined questions.

The methodology composition work (multi-manifest loading) is, viewed
from this angle, building toward a higher category — where each
methodology is itself an object, and the relations between them are
themselves structural maps. Layer 3 lives here.

## The Threshold

The work of building toward Layer 3 appears to cross a threshold that
should be named explicitly, because the layer-progression framing
alone obscures it. The framing in this section is contingent — it is
our current sharpest approach to a distinction we sense is real, not
a settled answer. The artifact-and-protocol audit (pre-work item 1)
is the empirical test, and the framing is expected to evolve under
that test.

The threshold is in **what the substrate can soundly infer from the
existence of a typed value.**

Below the threshold, the type system classifies content. A type tells
you what kind of artifact you have. Type-checking happens at protocol
dispatch: the substrate sees an incoming artifact, checks whether its
declared type matches what the protocol expects, dispatches if so.
The artifact is real and may be highly structured; the cognitive work
that produced it is real and durable. What the substrate cannot do is
infer anything about *how* the artifact was produced from the fact
that it exists with a given type. If an artifact appears claiming to
be a `ValidatedHypothesis`, the substrate trusts the claim. The
artifact's own content is the warrant; the substrate's reading is
classification.

Above the threshold, the type system also serves as **evidence about
production**. Specific structural enrichments make this possible:

- **Constructor gating** — the type's only constructors are specific
  protocols. No other path produces a value of that type. Existence
  of a value of `ValidatedHypothesis` is then itself information:
  the Validate protocol must have run.
- **Refinement predicates** — properties a value must satisfy to
  inhabit the type, checked structurally rather than asserted in
  content.
- **Provenance carrying** — the type identity includes how the value
  was constructed (`ValidatedHypothesis[via Validate, with Evidence
  E]`).
- **Algebraic composition that preserves these guarantees** — a
  product of two evidence-bearing types carries forward both
  witnesses; a sum carries forward whichever was constructed.

What changes at the threshold is not whether artifacts are real or
whether they have structure. Both sides have real, structured
artifacts. What changes is whether *existence-of-the-typed-value is
itself information* the substrate can soundly act on.

The threshold cannot be crossed by working harder on what already
exists. The enrichments above are not refinements of dispatch-time
classification; they are different mechanisms with different
requirements. Layer 2 is precisely this enrichment of the substrate.
It is not an enhancement of the artifacts or of the cognitive work
that produced them; it is an enrichment of the substrate's inference
power.

Two properties of this threshold are worth noting because both are
counterintuitive.

**It has a direction.** A substrate with evidential typing can
trivially provide classification typing (read evidence-bearing values
as if they were mere classifications). The reverse is not true.
Classification typing cannot grow into evidential typing without the
structural enrichments above. This makes the threshold asymmetric in
a way that ordinary engineering progressions are not.

**It does not require a different kind of cognizer.** The temptation
is to imagine that the further side requires "more capable agents" or
"different kinds of agents." This frame imports an entity that is
itself a convenience — when we say "the agent does cognition" we have
already labeled a token-transformation as agentic activity. The
transformer below the threshold and the transformer above the
threshold are doing token transformation. What is different is what
the substrate makes of what the transformer produces. "Agent" is a
manifestation of the transformer in interaction with the substrate,
not a fixed thing that crosses the threshold.

A flag worth keeping visible: the threshold may not be a single
threshold. Constructor gating, refinement, and provenance carrying
are often grouped together in type theory but it is not obvious they
flip together at a single moment. It is also not obvious that all
three are required for the cross-domain unification claims made
about Layer 3. The artifact-and-protocol audit may surface that what
we are calling one threshold is actually a cluster of related
transitions. That is acceptable; the framing should hold as approach,
not as committed structure.

The implications of the threshold are large enough to warrant
distinct treatment: certain cognitive forms appear to require
evidential typing to be expressible at all. Paraconsistent reasoning,
homotopic reasoning, and resolution-parameterized understanding are
candidate examples — their definitions seem to require inhabitants
in a substrate whose typing carries evidence about construction, not
labels on content. Whether this is actually true, and whether all
three require the threshold to be fully crossed, is among the
questions the pre-work is meant to test.

## The Three Layers

Mapped onto the threshold:

### Layer 1: Classification typing (have it)

A category C of artifact types and protocols. Runtime type-checking at
protocol dispatch (runa enforces that input artifact type matches
protocol expectation). Composition via the dependency graph.
Methodology as the signature defining which C is in scope for a given
run.

This is classification typing fully realized: the substrate reads
artifacts as typed instances and dispatches accordingly, but does not
infer anything about the artifact's production from its existence
with a given type. The categorial structure already exists; what was
missing was the vocabulary to name it. Tesserine, today, is a typed
cognitive state machine at the classification layer.

### Layer 2: The threshold (gap is substrate enrichment)

The work of giving the substrate the structural mechanisms by which
existence-of-a-typed-value becomes evidence about production.
Candidate enrichments (likely interrelated, possibly separable):

- **Refinement types** so `ValidatedHypothesis` is structurally
  distinguishable from `Hypothesis` rather than asserted in content
- **Algebraic data types** (products, sums, recursion,
  parameterization) for composite artifacts that preserve evidence
  through composition
- **Constructor discipline** so a `ValidatedHypothesis` value can
  only be produced by the Validate protocol — gating inhabitation
  of the type to specific protocols
- **Provenance carrying** as part of type identity, where the type
  records how a value was constructed rather than only what kind it
  is

Layer 2 is not a layer of capability stacked on Layer 1; it is the
work that crosses the threshold. After Layer 2, the substrate can
soundly act on the existence of typed values as evidence about how
they were produced. The artifacts and the transformer producing them
have not changed; what the substrate can infer from them has.

Once the threshold is crossed, the audit trail becomes the typed
artifact graph itself; substrate inference replaces narrative
forensics for facts the typing covers.

### Layer 3: Evidential substrate proper (gap is the higher category)

Once the substrate's typing carries evidence about production,
methodologies become objects in a higher category — and **functors
and natural transformations between methodologies become definable.**
At this layer:

- An improvement in one methodology can mechanically transfer to
  another via the relating functor
- Two methodologies can be proven structurally equivalent or
  non-equivalent
- New methodologies can be synthesized from compositions of existing
  ones
- Cross-domain unification (medical diagnosis, software debugging,
  legal investigation as instances of one higher-order cognitive type)
  becomes possible
- Certain cognitive forms — paraconsistent reasoning, homotopic
  reasoning, resolution-parameterized understanding — become
  expressible if they require evidential substrate to have meaning,
  which we believe but have not verified

Layer 3 is the level at which cognition becomes a mathematical
substance the substrate computes with — not merely a flow of typed
records the substrate dispatches.

## What This Trajectory Means

Tesserine's positioning shifts under this framing.

It is not "an autonomous AI agent infrastructure" — that description
captures Layer 1 operationally but misses what the substrate enables.
It is the foundational substrate for cognition as an engineering
discipline: a place where reasoning is composable, verifiable,
refactorable, and provably equivalent across instances. The container
metaphor (agentd:containerd, runa:runc) describes the operational
shape; the categorial framing describes the cognitive shape; the
threshold framing describes the trajectory across which the
substrate's inference power changes character. All three are true
together. None alone is sufficient.

If the trajectory across the threshold is what we currently believe
it to be, the shift is the same order as the shift from alchemy to
chemistry: from accumulating empirical recipes that classify
cognitive workflows to deriving them from a typed substrate whose
composition laws carry evidence about the workflows themselves.
That claim is large, and it depends on the threshold framing being
empirically grounded — see open question #7.

## Open Questions

These are not yet reckoned and should not be treated as decided.

**1. Runtime vs. static type-checking.** Layer 1's type-checking
happens at runtime in runa. Layer 2's witnesses could be
runtime-checked or statically-checked. These are different shapes of
work and different research bets. The choice depends on what
trade-offs matter (development speed, error-detection earliness,
tooling ecosystem) and what's available.

**2. The vehicle for Layer 2.** Is the right move to enrich the
existing artifact-type machinery in place, or for runa to grow a small
type *system* (not just type *checking*)? These are different
magnitudes of work and different invasiveness levels.

**3. Operational return on Layer 2.** What does artifact-as-witness
buy in practice? If three specific cases can be named where its
absence currently bites or its presence would enable something new,
the case is grounded. If not, Layer 2 risks being elegant theory
without operational return.

**4. Operational return on Layer 3.** Same test. What specific value
does a functor between methodologies provide — to a user, an operator,
an integrator? If speculative, Layer 3 is research direction, not
roadmap.

**5. Relation to in-flight v0.1.1 work.** Audit trail (#76), exit
codes epic, protocol coherence audit (#213) — does the typed-cognition
trajectory complement, redirect, or supersede any of them? Without
this reconciliation, the document floats apart from current execution.

**6. Day-One alignment.** Does the trajectory strengthen the
foundation, or represent gold-plating? Initial reckoning suggests
strengthening, but that deserves explicit verification rather than
assertion.

**7. The threshold framing itself.** The classification-vs-evidential
distinction is offered as the orienting framing for the entire
document. It is the third sharpening of this framing in successive
reckoning passes (after "Layer 1 → Layer 3 progression" and
"descriptive vs. constitutive typing"). Each pass has felt like
arrival; each has revealed loose edges under pressure. The framing
in this draft is the current sharpest approach, not a settled answer.
It needs validation: does the threshold hold across the actual
artifact types and protocols Tesserine uses? Is what we are calling
one threshold actually a single threshold, or a cluster of related
transitions that group together in theory but separate in practice?
The artifact-and-protocol audit (item 1 of pre-work) is the
empirical test, and the framing should be expected to evolve under
that test rather than be defended.

## Pre-Work

Before this draft can become a committed commons-level foundation
document, the following reckoning sessions are required. Each becomes
its own session whose output feeds the eventual synthesis.

1. **Tesserine artifact-and-protocol audit.** Map every actual
   artifact type and protocol against the categorial vocabulary.
   Identify irregularities. Confirm that what exists actually forms a
   category cleanly, or surface where the metaphor breaks. Empirical
   test for the threshold framing.

2. **Layer 2 grounding.** Identify three concrete cases where
   artifact-as-witness would prevent a real failure or enable a real
   capability. Without this, Layer 2 is theory.

3. **Layer 3 grounding.** Identify what specific value a functor or
   natural transformation provides in operational terms. Without this,
   Layer 3 is speculation.

4. **Runtime-vs-static reckoning.** Examine the trade-offs explicitly
   with criteria for resolution.

5. **In-flight work alignment.** Reconcile the trajectory with current
   v0.1.1 work. Identify which committed work is on the trajectory,
   which is orthogonal, and whether anything is in tension.

6. **Light external survey.** Comparable work in PL theory, typed
   agent architectures, cognitive frameworks. Not to copy, but to
   know context and use right vocabulary where prior art has good
   vocabulary.

7. **Audience clarification.** Who is the eventual document for?
   Internal Tesserine contributors? External developers evaluating the
   project? Future Claude/Codex instances orienting on the system?
   The document's depth and assumed background depend on the answer.

8. **Day-One alignment confirmation.** Explicit reckoning that the
   trajectory strengthens rather than constrains the foundation.

## What This Document Is For

This draft captures the conceptual breakthrough of the April 24
sessions before it cools. It is not yet authoritative. It is:

- **Aide-mémoire** preserving the reckoning so it persists across
  context boundaries
- **Seed** for the pre-work sessions enumerated above
- **Scaffold** that the eventual commons-level document will inherit
  from

The texture of how the framing emerged — through the specific
reckoning move that recognized the artifact as the cognitive state
itself, the subsequent move that named a threshold between
classification and evidential typing, and the later sharpening that
located the threshold in what the substrate can soundly infer from
the existence of a typed value rather than in any change to the
cognizer — is itself part of what the eventual foundation document
needs to teach. That texture lives here for now, held as approach
rather than arrival.

---

*The default is for the type system to classify what the substrate
sees. The shift is for the typing to carry evidence about how what
the substrate sees came to be. The threshold is not in the cognizer;
it is in what the substrate can soundly infer from the existence of
a typed value.*
