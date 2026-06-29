# Roadmap Graph

**Stratum:** Conventions · [Register](README.md)
**Domain:** Work tracking
**Rooted in:** [Single Home](https://github.com/pentaxis93/principles/blob/main/principles/single-home.md) · [Sovereignty](https://github.com/pentaxis93/principles/blob/main/principles/sovereignty.md)

> **The convention.** Each repository has exactly one roadmap issue. That issue
> is the canonical entry point and the sole authoritative home of the repo's
> work-unit graph; individual work-unit issues carry their own content, not the
> graph's structural edges.

## The rule, precisely

A repo's roadmap issue is the durable graph state for work in that repository.
Every actor who needs the work-unit graph starts there, reads the present graph,
and changes the graph by changing that issue body. Work-unit issues remain the
home of local unit content: problem statement, acceptance criteria, discussion,
evidence, and landing notes. They do not own graph structure. If a unit issue
mentions sequencing, dependency, or epic context, that mention is explanatory;
the graph edge lives only in the roadmap.

One repo therefore has one graph home, not a graph spread across labels,
milestones, issue sidebars, cross-linked comments, and individual unit bodies.
The roadmap is the place where order, membership, state, and unplaced work can
be read at a glance.

## Body format

The roadmap body is line-oriented. Each work line starts with the most stable
identifier available for the unit:

- Materialized unit: `#N — Title`
- Frontier operation not yet ticketed: `<operation> → <pointer> — Title`

For a materialized unit, the issue number comes first and the title is always
present. For a frontier operation, `<operation>` is a named act such as
`decompose`, `survey`, `reckon`, `research`, `issue-craft`, or
`reframe-as-spike`, and `<pointer>` names the spec location the act works on.

Sequence is shown by order in the roadmap plus an explicit annotation when the
order has a reason:

- `needs #N` marks a technical dependency.
- `after #N · by design` marks intentional sequencing that is not a technical
  dependency.

Epic membership is shown by indentation beneath the epic line. Landed units are
marked with `✓` before the issue number, so done and pending work separate at a
glance. Every roadmap keeps a standing `Unplaced` section for work units that
exist but have not yet been given a graph position.

The format expresses the work-unit state spectrum:

- frontier-op: no issue exists yet, so the line is `operation → pointer — Title`
- stub: an issue number exists, but the unit is committed and not yet fully
  specified
- spec'd unit: an issue number exists and the body is ready to execute
- landed: the line is marked as landed, for example `✓ #N — Title`

## Example

```text
#32 — Roadmap graph epic
  #33 — Author the roadmap convention
  #34 — Convert the epic roadmap to the convention (needs #33)
  #35 — Wire roadmap maintenance checks (after #33 · by design)

research → docs/graph-maintenance.md — Survey graph maintenance failure modes

Unplaced
  #41 — Candidate unit waiting for graph placement
```

The example is illustrative; the convention is the body grammar above, not this
specific set of sections or titles.

## Boundaries

- The roadmap issue owns graph structure: sequence, dependency annotations,
  epic membership, landed state, and the Unplaced queue.
- A work-unit issue owns unit content: scope, acceptance criteria, discussion,
  evidence, and landing record.
- Labels, milestones, project boards, and backlinks may aid discovery, but they
  are not the authoritative graph and must not become a second structural home.
- The convention governs the per-repository graph. Cross-repository planning can
  cite per-repo roadmaps, but it does not move a repo's work-unit graph out of
  that repo's roadmap issue.

## Relations

- **operationalizes** — *State is the interface*
  ([fleshed](../golden-rules/state-is-the-interface.md)): the graph is durable,
  legible issue-body state that actors read and write rather than carrying a
  private plan.
- **roots** — Single Home, Sovereignty (above): the graph has one home, and the
  boundary between roadmap-owned structure and unit-owned content stays clean.

## Sources

- Founding work-unit: `pentaxis93/commons` #33.
- Framing epic: `pentaxis93/commons` #32.
