# Right Action

**Stratum:** Golden Rules · [Register](README.md)
**Domain:** The shape of work
**Rooted in:** [Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md) · [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md) · [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md) · [Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md)

> **The rule.** Right Action is the **single operation** that becomes correct by
> reading the state it is in. It reads what is true, infers what is needed from
> the actual/desired gap, and does exactly that — no script of steps, no plan
> held in reserve. Run again, it reads again; if the gap remains, it continues to
> converge; if the state is settled, it changes nothing.

## The rule, precisely

The unit of work is one **idempotent** operation. Its correctness is not a
property it carries in — not a plan it brings, not a sequence it remembers — but
one it *acquires* by reading the present state and fitting its action to what it
finds. It reads what is true (the state), computes the gap between what is and
what is needed, and applies exactly the action that closes that gap: nothing
pre-scripted, and nothing beyond what the gap demands. Because the work is
derived from the gap rather than from a held plan, repetition is safe — a second
run reads the now-current state, finds the gap closed or smaller, and acts only
on what remains. That is the idempotence: not "remembers that it ran" but "reads
fresh and acts only on the outstanding gap," so running again converges rather
than accumulates. Once the state is settled, a rerun is a no-op.

The name marks the stance — action made right by its **fit to the present**,
sufficient and bounded, derived from the state rather than imposed on it. It
borrows nothing else: no ethical doctrine and no appeal to a tradition as the
architecture's authority, which rests entirely on the principle roots and the
convergence evidence below.

## Rooted in principles

This rule cites the universals beneath it; it does not contain them, and it is
not one of them.

- **[Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md)** — *every inference earns its chain.* Right Action reads
  its work from the state, where the truth is written and auditable, and holds no
  private plan — so there is nothing off-chain. What it does traces to what it
  read; a worker that acted from a plan held in its head would have a conclusion
  with no chain back to ground.
- **[Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md)** — *completion is an observable state;
  the evidence comes first.* The operation's read-step **is** *verify before
  act*: it checks the state and acts only on the outstanding gap, so "done" is
  read off the state, never asserted by the worker. This is also the structural
  source of the idempotence — acting only on the gap is exactly what makes a
  rerun against a settled state a no-op.
- **[Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md)** — *repair the class at the origin, then
  regenerate downstream.* Because Right Action derives its work from current
  state, it is safe to **re-run after a source repair**: it reads the corrected
  reality and converges, rather than replaying a stale plan built on the broken
  substrate. Convergence-not-accumulation is the operational face of
  regenerate-from-the-repaired-source — the reason a known-broken run can simply
  be run again.
- **[Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md)** — *one side owns what must be true, the other how it
  becomes true; authority attaches to the role, not the act of invocation.* Right
  Action names no host and holds no embedded plan: authority lives in the state
  (the WHAT), and the operation supplies only the capacity to read it and
  converge (the HOW). It is therefore maximally swappable — the same operation,
  run by any actor, at any time, against the same state, does the same fitting
  thing. Sovereignty's *mode is a property of the session, not the operation*
  projection is this exactly: the verb's meaning and authority do not change with
  who invokes it.

## The invariant beneath

A golden rule earns its standing by instancing a structure deeper than itself —
a principle beneath, a master above. The structure this rule projects:

> A unit of work that holds no plan of its own becomes correct by reading the
> present state, inferring the needed work from the gap between what is and what
> is required, and applying exactly that — so that repeating it converges on the
> settled state rather than accumulating change.

Reduced to its loop:

```
read state → infer the gap (actual vs. needed) → apply the fitting action → re-read
         ↑________________________________________________________________|
              gap closed → no-op   ·   gap remains → converge
```

— the operation carries nothing between runs; the state carries the work, and
convergence is what repetition produces.

This structure is not a software convenience. It is the **reconciliation** /
level-triggered control loop independently arrived at across declarative
infrastructure — observe the actual state, compare to the desired, act to close
the difference, idempotently and repeatably — and, outside computation, it is
rhymed by the contemplative discipline of action that fits the present moment.
That wholly different domains realize the same structure is the evidence the
structure is **objective** rather than a local habit, which is what lets this
rule stand as a golden rule and not merely a preference.

## Domain and scope

The rule governs work that can be shaped as a **single operation over a durable,
readable state**, where its load-bearing conditions hold: the needed end-state
can be expressed or inferred, the operation can compute its work from the
**actual/desired gap**, and its effects **converge** — re-applying to a settled
state is a no-op. Where the state is not readable or durable, or the work is
irreducibly sequential and non-convergent (irreversible side effects that cannot
be made gap-derived), "do what the state needs" cannot be made idempotent, and
forcing the shape there manufactures complexity rather than removing it.

Scoped this way, the rule covers a daemon reconciling a system, a one-shot
operator action, a nightly processor, an agent's work-step, and a protocol
handler alike — the gap-derivability and convergence of the operation, not its
cadence or the number of actors, are what the rule turns on. (As with the medium
in *State is the interface* and the stability differential in *Architectural
layers bounded by contracts*, the rule turns on a structural condition, not on
the deployment unit.)

## What the rule requires

Idempotence is a property the operation must be **built to have**; it is not
free. A lawful Right-Action operation therefore reads the state **fresh** each
run (no cached plan, no memory of the last run standing in for the state);
**derives its work from the gap**, not from a script (so a changed reality
changes the work); **checks before it acts** (applying only the outstanding
delta, so a settled state yields a no-op); and carries **bounded validity** —
not every gap is a valid gap to close. A corrupt or malformed state presents
pressure, and the operation must be bounded against answering it, exactly as
*State is the interface* requires of state-pressure. These are the rule's
idempotence-and-convergence half made explicit: read-fresh, gap-derivation,
check-before-act, and bounded validity together are what make "run again" mean
*converge* rather than *repeat the damage*.

## Boundaries

- This rule is **not "state is the interface."** That components meet only in
  durable state is the *medium* they coordinate through (the sibling rule *State
  is the interface*); Right Action is the *act on* that medium — the single
  operation that reads it and converges. The medium and the act are distinct
  rules a system holds together.
- This rule is **not "architectural layers bounded by contracts."** That
  dependencies run toward the stable contract is the *boundary and direction*
  across a layer seam (the sibling rule); Right Action is the *unit of work* that
  runs across the layers. A contract is the surface; Right Action is an act that
  reads it and satisfies it.
- **"Right" is fit to the state, not a moral or universal verdict.** The rule
  names action made correct by reading what is present — the surfer reading the
  wave, not a precept. It imports no ethical doctrine and makes no tradition the
  architecture's authority.
- **"No held plan" is not "no structure."** The structure is in the operation's
  logic — *how* to read the state and compute the fitting action — while *what*
  to act on is read off the state. Right Action is disciplined, bounded,
  sufficient action, not improvisation.
- **Idempotent where convergence is achievable, not a universal mandate.** Some
  work is irreducibly sequential or side-effecting; the rule applies where the
  operation can be made gap-derived and convergent, never as a demand that all
  work be forced into one idempotent move.

## Cross-domain evidence: convergent reconciliation and the fitting act

The invariant this rule projects was not invented; it was independently arrived
at across declarative infrastructure, which is the strongest evidence it is
objective. A **Kubernetes** controller observes the actual state of the cluster,
compares it to the declared desired state, and acts to converge the two —
running continuously and idempotently, so that a reconcile against an
already-settled state changes nothing. The same structure is **Terraform**'s
plan-and-apply (declare the desired state; apply converges; a re-apply with no
drift is a no-op), **Ansible**'s idempotent modules, **Puppet** and **Chef**'s
desired-state convergence, and **Nix / NixOS**'s declarative rebuild. Independent
arrival at one shape — *declare or infer the end-state; an idempotent operation
reads the gap and converges* — by people not copying one another is what
distinguishes an objective invariant from a local convention. It is directly
groundable from the public canon, with no sovereign evidence commission needed.

The formal core is **mathematical idempotence**: an operation `f` for which
`f(f(x)) = f(x)` — applying it twice equals applying it once. Reconciliation
makes the work **level-triggered** (act on the present gap) rather than
edge-triggered (act on a remembered event), which is why a missed run, a repeated
run, or a run from an unknown starting point all still converge.

Outside computation, the same shape is rhymed by the contemplative stance of
**action that fits the present** — the *nondual responsive action* (Daoist
*wu-wei*) that the sibling rule *State is the interface* already cites as
evidence. The actor meets the present carrying no plan and answers what is
actually there: action arising from the situation rather than imposed on it, the
fit that costs no force — Bruce Lee's "be like water," which takes the shape of
its vessel and does only what the moment needs. This corroborates the *stance* —
fitting, unforced, state-derived action — and the **non-accumulation** facet:
each act complete in itself, nothing carried forward, the way a bead is told and
released. It is honest only that far. As the eterne analysis records, *exact*
mathematical idempotence is **rhymed by non-clinging, not carried by it** — the
contemplative pole supports the stance, not the formal convergence property,
which stands on the reconciliation canon and the principle roots.

The convergence canon and the formal idempotence are the load-bearing
cross-domain evidence; the contemplative resonance is cited as evidence the
invariant is objective, **never as the rule's authority**. "Right Action" names
the fitting, state-derived act; it does not make any tradition the
architecture's authority — that rests on the roots above and the
reconciliation/idempotence evidence here.

## Relations

- **sibling** — *State is the interface* ([fleshed](state-is-the-interface.md)):
  the medium components meet in; Right Action is the act that reads that medium
  and converges. The medium and the act are two rules, not one.
- **sibling** — *Architectural layers bounded by contracts*
  ([fleshed](architectural-layers-bounded-by-contracts.md)): the boundary between
  layers and the direction of dependency across it; Right Action is the unit of
  work that runs across them — the contract is the surface, Right Action an act
  that satisfies it.
- **relation (operational cycle)** —
  [Completed Noticing](https://github.com/pentaxis93/principles/blob/main/compositions/completed-noticing.md):
  Right Action is a single turn of the noticing cycle made one repeatable
  operation — read the state (Attend) → infer the gap (Verify) → apply the
  fitting action (Respond) → leave the changed state the next run reads, holding
  nothing of its own (Release, non-possessive) → run again (Repeat). Completed
  Noticing is the *cycle*; Right Action is its *unit*, and the bead loop is that
  unit repeated — the corpus side of the cognitive-state-machine ↔ Completed
  Noticing edge.
- **roots** — Traceability, Verifiable Completion, Source Repair, Sovereignty
  (above).

## Sources

- Root principles: [Traceability](https://github.com/pentaxis93/principles/blob/main/principles/traceability.md), [Verifiable Completion](https://github.com/pentaxis93/principles/blob/main/principles/verifiable-completion.md), [Source Repair](https://github.com/pentaxis93/principles/blob/main/principles/source-repair.md), [Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md) — `pentaxis93/principles`.
- Related composition: [Completed Noticing](https://github.com/pentaxis93/principles/blob/main/compositions/completed-noticing.md) — `pentaxis93/principles` (the operational cycle whose single repeated turn this operation is).
- Cross-domain evidence: the reconciliation / level-triggered control loop — the Kubernetes / Kubebuilder reconciliation model, Terraform plan-and-apply, Ansible, Puppet, Chef, and Nix / NixOS declarative convergence; and mathematical idempotence (`f ∘ f = f`). The contemplative resonance — the *nondual responsive action* (wu-wei) analysis homed in `pentaxis93/eterne` `vault/archives/intelligence/research/research-2026-06-29-state-interface-contemplative-isomorphism.md`, consulted not restated; honest that exact idempotence is rhymed-not-transferred.
- Founding capture: this stratum's seed for the rule (`pentaxis93/commons` #19).
