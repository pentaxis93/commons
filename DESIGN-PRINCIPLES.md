# Design Principles

Engineering judgment for the pentaxis93 ecosystem. These principles sit
between the bedrock principles (PRINCIPLES.md) and project-specific ADRs —
they govern how we think about code across all repos.

Each principle was learned through friction: review rounds that revealed
architectural mistakes, bugs that traced back to design decisions, or
patterns that emerged across multiple projects.

---

## Elimination over accommodation

### 1. One mechanism, not two

When two systems must agree, make them one system. Two filters that must
stay in sync will diverge. Two sources of truth for the same decision will
contradict. If a remediation patches a second filter to match a first,
look for the architectural fix that eliminates the class.

### 2. Eliminate the class, not the instance

When a fix makes a subsystem smarter about one more edge case, ask whether
the subsystem should exist. The recognition signal: "each fix makes the
subsystem smarter about one more edge case without eliminating the class of
bug." If the pattern is visible by round 3-4, name it — don't wait for
round 10.

### 3. Computed over stored for derived state

If the source of truth is available at query time, derive the answer
instead of storing it. Stored derived state goes stale, creating
consistency bugs and meta-staleness problems.

### 4. Policy over status tracking

When a status is always true by convention, enforce it as policy rather
than tracking it. Eliminates a state dimension and the engine complexity
to manage it.

---

## Fix at the source

### 5. Silent code teaches louder than docs

Code that silently accepts a condition models that condition as acceptable.
Agents and reviewers follow the code's model, not the documentation's
disclaimers. When code and docs disagree about what's supported, fix the
code — that's where the false signal originates.

### 6. Trace assumptions to their origin

When a reviewer or agent makes a wrong assumption, trace it back to the
code or artifact that created it. The surface correction is documentation;
the real fix is at the source. Issues are seeds — contamination in the
seed propagates through the plan into the implementation with perfect
fidelity.

### 7. Fixes belong at discovery, not deferred

One fix now prevents compounding friction across every future change. A
known problem deferred accumulates interest. Silence in the face of a
known problem is complicity with that problem.

---

## Honest naming and structure

### 8. Name what it is, not what you wish it were

Borrowed prestige inflates architecture. Honest naming compresses to the
real shape. If a layer exists only because an adjacent system has one,
it doesn't earn its place.

### 9. Fail explicitly, never silently

Silent degradation paths create false assumptions about what's supported.
Explicit failure is clearer than graceful degradation — it prevents
downstream systems from building on capabilities that don't exist.

---

## Correctness over optimization

### 10. Ship correct, then optimize

Pre-v1.0, correctness matters more than avoiding wasted work. An
optimization that introduces a correctness gap is a regression. Wasted
work produces identical output; incorrect optimization produces wrong
output.

### 11. Omit rather than half-implement

A deferred feature is better than a half-correct one. The instinct to
"complete all acceptance criteria" is weaker than the instinct to ship
correct code.

---

## Architecture as communication

### 12. Self-maintaining over maintainer-dependent

Prefer architectures where the system maintains itself. Runtime resolution
over build-time embedding. Upstream verification over local verification
files. A self-maintaining design is better than a maintainer-dependent
design, even if less elegant.

### 13. Spec and implementation are separate scopes

A boundary spec defines the interface. The work to implement it is a
separate scope. Mixing them confuses executors — the agent cannot
distinguish constraints from descriptions.

### 14. Ground to needs, not to code

Code is current state, not ground truth. Ground to what is needed, then
compare code to what needs require. Treating what the system currently does
as the definition of what it should do is the most common grounding failure.

---

## Review discipline

### 15. Fix is the default disposition

Accept must be acceptable permanently — not "we'll address it holistically
later." Defer requires an issue so it doesn't pass silently. When in doubt,
fix.

### 16. Squash-on-merge at the boundary

Session history lives in session notes. Repo history lives in git. One
clean feature per merge. The commit history tells the story of convergence;
the repository history tells the story of capability.

---

*Each principle was extracted from a concrete mistake. The mistake is the
teacher; the principle is the lesson encoded so the mistake need not repeat.*
