# Roadmap Graph

**Stratum:** Conventions · [Register](README.md)
**Domain:** Work tracking
**Rooted in:** [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) · [Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md)

> **The convention.** The work-unit graph is homed as **nested roadmaps** — an
> outline whose nodes nest. Each roadmap node — a repo roadmap, an epic — is the
> single home of its **immediate children's** membership and same-parent
> sequence, and lists only those children, never the transitive sub-graph. A
> dependency whose endpoints sit in different branches is homed in the roadmap of
> their **nearest common ancestor**. Single Home holds by *partition*, not by
> centralization.

## The rule, precisely

A roadmap is not one issue per repo holding the whole graph; it is an **outline
that nests**, a roadmap-of-roadmaps. The graph is partitioned across the
containment hierarchy, and each piece has exactly one home.

- **Each node homes its immediate children only.** A roadmap node — a repo
  roadmap or an epic — is the single home of the membership and same-parent
  sequence of the children *directly* beneath it, and it lists only those. An
  epic body lists its immediate child units; a repo roadmap lists the repo's
  epics and top-level units, not the epics' children; the nesting continues
  upward through the containment hierarchy. A unit's own content — problem
  statement, acceptance criteria, discussion, evidence, landing record — stays in
  the unit's own issue.

- **Single Home by partition.** Every edge in the graph has exactly one home,
  and the home is determined by the edge's class. A *membership* edge and a
  *same-parent sequence* edge are homed in the parent node. A *cross-branch
  dependency* edge — endpoints in different branches — is homed in the roadmap of
  the **nearest common ancestor**: the lowest node that contains both endpoints.
  No edge is duplicated, and no node flattens the graph beneath it. Reading any
  node shows its immediate composition; the whole graph is read by descending.

- **The containment hierarchy is the stature ladder.** Nodes nest along the
  existing inheritance ladder: `pentaxis93/commons` (universal base) →
  `tesserine/commons` (ecosystem) → repository → epic → sub-epic / unit. The
  nearest common ancestor of two units is found by ascending this ladder from
  each until one node contains both. A same-parent dependency is the trivial
  case — the parent *is* the common ancestor, so the edge is homed there.

- **Navigation is hierarchical, top-down.** A reader reaches a live work unit by
  descending from the top through active links, following only active branches.
  Each roadmap cites its child roadmaps by link rather than absorbing their
  content; the descent stops at the unit issue, which holds the work itself.

## Body format

A roadmap node's body is line-oriented and lists its **immediate children**.
Each work line starts with the most stable identifier available for the child:

- Materialized unit: `#N — Title`
- Frontier operation not yet ticketed: `<operation> → <pointer> — Title`

For a materialized unit, the issue number comes first and the title is always
present. For a frontier operation, `<operation>` is a named act such as
`decompose`, `survey`, `reckon`, `research`, `issue-craft`, or
`reframe-as-spike`, and `<pointer>` names the spec location the act works on.

Sequence among same-parent children is shown by order plus an explicit
annotation when the order has a reason:

- `needs #N` marks a technical dependency on a same-parent sibling.
- `after #N · by design` marks intentional sequencing that is not a technical
  dependency.

Membership is shown by indentation beneath the parent line. Landed units are
marked with `✓` before the issue number, so done and pending work separate at a
glance. Every roadmap keeps a standing `Unplaced` section for child work units
that exist but have not yet been given a position.

A **cross-branch dependency** — whose endpoints are not same-parent siblings —
is recorded only at its nearest-common-ancestor node, in a `Cross-branch`
section that names the edge by its endpoints (`#A needs #B — why`). The endpoints
are named, not re-listed as members: their membership stays in their own parent
nodes. A node never restates an edge homed above or below it.

The format expresses the work-unit state spectrum:

- frontier-op: no issue exists yet, so the line is `operation → pointer — Title`
- stub: an issue number exists, but the unit is committed and not yet fully
  specified
- spec'd unit: an issue number exists and the body is ready to execute
- landed: the line is marked as landed, for example `✓ #N — Title`

**Rendering.** A roadmap node's listing is written in Markdown and is **not** wrapped in a code fence: every identifier must render as a **live link**, because navigation is by descending those links, and a fenced listing renders link-dead and breaks the descent. A same-repo `#N` autolinks; a cross-repository reference is written `owner/repo#N` (which autolinks) or as an explicit Markdown link.

## Example

A repo roadmap lists the repo's epics and top-level units — its immediate
children — and homes the cross-branch edges among their descendants:

**`acme/widgets` — roadmap**

- acme/widgets#10 — Storage epic
- acme/widgets#20 — API epic
- acme/widgets#31 — Adopt the house style guide — after acme/widgets#10 · by design

*Cross-branch*

- acme/widgets#24 needs acme/widgets#13 — the API serializer needs the storage schema

*Unplaced*

- acme/widgets#45 — Telemetry spike (awaiting placement)

One of those epics is itself a roadmap node, listing only *its* immediate
children and their same-parent sequence:

**acme/widgets#20 — API epic — roadmap**

- acme/widgets#22 — Define the API contract
- acme/widgets#23 — Implement the handlers — needs acme/widgets#22
- acme/widgets#24 — Add the serializer — needs acme/widgets#23

The same-parent edges `#23 needs #22` and `#24 needs #23` live in the epic that
parents them. The cross-branch edge `#24 needs #13` — `#24` is under `#20`, `#13`
is under `#10` — is homed one level up, at the repo roadmap, the lowest node
containing both branches. Neither the repo roadmap nor the API epic re-lists the
other's members.

The example is illustrative; the convention is the nested partition and the body
grammar above, not this specific set of nodes or titles.

## Boundaries

- A roadmap node owns the structure of its **immediate children**: their
  membership, same-parent sequence, landed state, and the node's Unplaced queue.
  It does not own a descendant node's internal structure — that is the
  descendant's to home (Single Home by partition).
- A cross-branch dependency edge is owned by the **nearest-common-ancestor**
  roadmap and recorded only there; no other node restates it.
- A work-unit issue owns unit content: scope, acceptance criteria, discussion,
  evidence, and landing record. It carries no structural graph edges; a unit's
  mention of sequencing or dependency is explanatory, while the edge itself lives
  in the owning roadmap node.
- Labels, milestones, project boards, and backlinks may aid discovery, but they
  are not the authoritative graph and must not become a second structural home.
- Cross-repository dependencies are the general case of the nearest-common-ancestor
  rule: their home is the lowest roadmap up the containment ladder that contains
  both repositories' branches (for example `tesserine/commons`, or
  `pentaxis93/commons` at the base), not a copy duplicated into each repo's
  roadmap. A higher-level roadmap cites the per-repo roadmaps beneath it by link;
  it does not absorb their graphs.

## Relations

- **operationalizes** — *State is the interface*
  ([fleshed](../golden-rules/state-is-the-interface.md)): each roadmap node is
  durable, legible issue-body state that actors read and write rather than
  carrying a private plan; the nesting is the partition that keeps that state
  single-homed as the graph grows.
- **roots** — Single Home, Sovereignty (above): every edge has exactly one home
  by partition, and the boundary between roadmap-owned structure and unit-owned
  content stays clean.

## Sources

- Founding work-unit: `pentaxis93/commons` #33 (the flat model this supersedes).
- Nested-model rewrite: `pentaxis93/commons` #39.
- Framing epic: `pentaxis93/commons` #32.
