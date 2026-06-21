# ADR Register

Architectural decision records for the pentaxis93 projects. This register is
the index; each ADR file is authoritative for its own content. A repository
implementing a decision links to the ADR — it does not restate it.

ADRs here record decisions that are *cross-cutting* — they apply across more
than one pentaxis93 project, which is the bar for anything living in this
repository. Repo-local decisions stay in their own repository.

| # | Title | Status | Traces to | Purpose |
| --- | --- | --- | --- | --- |
| [0001](0001-repository-merge-and-history-policy.md) | Repository Merge and History Policy | Accepted | Transmission (primary), Grounding, Parsimony | Active repos use squash-or-rebase merges (no merge commits) with enforced linear history where the plan permits; authors match method to pull-request shape; force-push protection, not the merge method, guards against history loss |

## Conventions

- Numbering is sequential and never reused.
- Status values: `Accepted`, `Superseded`. Partial supersession is stated on
  the Status line of the affected ADR.
- A new ADR adds its row here in the same change.
- The table has one row per `adr/*.md` decision file —
  `ls adr/*.md | grep -v README | wc -l` equals the row count (1).
