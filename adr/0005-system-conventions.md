# ADR-0005: System Conventions for Cross-Component Artifacts

**Status:** Accepted
**Traces to:** Principle 1 (Sovereignty) — primary; Principle 3 (Grounding) — secondary

## Decision

commons is the spec authority for artifact types that are system-level conventions. When an artifact type is meaningful across more than one methodology or more than one non-methodology consumer, its canonical definition lives in commons as a pair — a prose authority at repo root plus a versioned JSON Schema under `schemas/<artifact>/vN/`. Methodologies embed vendored copies at runtime with provenance metadata. Conformance between a vendored copy and its declared canonical version is an authoring-time governance check, not a runtime enforcement.

## Context

The Tesserine ecosystem has components that produce and consume the same artifact types across methodology boundaries. groundwork produces a request artifact today; agentd is being extended (agentd #81) to construct one without coupling to any specific methodology; runa orchestrates the sessions that consume it. When a producer's private schema is the only definition that exists, any methodology-agnostic consumer either couples to that producer or re-authors its own schema — either path creates drift and obscures which definition is authoritative.

commons already plays the spec-authority role for `EXIT-CODES.md`: a shared convention that neither runners nor callers own individually. Extending this role to schematized artifacts is a natural generalization, and it surfaces a set of decisions — where canonicals live, how they version, how methodologies adopt them, what reference forms count as conformance targets — that will recur whenever a new system-level convention emerges.

This ADR formalizes the pattern so future canonicalizations land consistently. The motivating instance is the request artifact, authored concurrently at `REQUEST.md` and `schemas/request/v1/request.schema.json`.

## Consequences

**Criteria for canonicalization.** An artifact type is system-level, and belongs in commons, when either (a) more than one methodology could reasonably implement it, or (b) more than one non-methodology consumer reads it — agentd, runa, operator tooling, auditing infrastructure. Methodology-private artifact types — meaningful only within one methodology's internal state — remain in that methodology.

**Canonical form.** Each canonical spec is a pair of artifacts: a prose document at repo root describing purpose, fields, semantics, version, stable identifier, and change policy (following the `EXIT-CODES.md` precedent); and a versioned JSON Schema under `schemas/<artifact>/vN/<artifact>.schema.json`. Both together constitute the canonical. The prose is authoritative; the schema is the mechanical realization of the prose.

**Disambiguating "canonical".** The word applies to the prose, to the schema, and to the pair interchangeably. When the prose and the schema disagree, the prose is authoritative and the schema is a defect to be corrected — not a competing interpretation. Review is the mechanism that catches divergence before it ships; runtime consumers of the schema are not expected to cross-check against the prose at validation time.

**Versioning.** Canonicals follow semantic versioning, with three levels of version information placed where each serves its purpose:

- **Major version maps to the directory.** `schemas/<artifact>/v1/`, `schemas/<artifact>/v2/`. This is the URL-stability boundary: once a major version ships, its path never changes shape and its content receives no breaking edits. Consumers using an old major version are not disturbed when a new one ships.
- **Full semver is the conformance target.** `1.0.0`, `1.1.0`, and so on. Stated in the prose header and in the schema's description field (or equivalent surface). Methodology vendoring provenance must name the full semver, not merely the major version.
- **Minor and patch edits are additive or clarifying only.** Removing fields, tightening required fields, narrowing accepted value spaces, or any other break against a conforming consumer requires a new major version — a new directory.

**Stable identifier.** Methodologies and cross-repo consumers must reference the canonical using an immutable URL form in any vendored-schema provenance or conformance declaration. Acceptable forms are commit-SHA URLs (`.../commons/<sha>/schemas/<artifact>/vN/...`) and release-tag URLs (`.../commons/<tag>/schemas/<artifact>/vN/...`). Mutable `main`-branch URLs are for human navigation only; a conformance claim against a moving target is not a conformance claim. Canonical machine identity lives in those immutable references, not in a schema-local URL token.

**Schema identity without `$id`.** Canonical schemas that do not need `$id` for cross-schema linkage omit it. This keeps machine identity aligned with immutable provenance and conformance references, avoids treating a mutable branch URL as canonical identity, and avoids coupling the authoritative schema to a specific hosting domain.

**Vendoring with provenance.** Methodologies that produce or consume a canonical artifact embed a copy of the canonical schema in their own `schemas/` directory with provenance metadata. Provenance must record, at minimum, the canonical URL in immutable form (commit-SHA or release-tag) and the full semver of the canonical version the vendored copy conforms to. How provenance is captured — file naming, sidecar file, comment header — is a methodology implementation detail; what must be recoverable is which canonical version the vendored copy matches.

**Authoring-time conformance.** A methodology's vendored schema must conform to its declared canonical version. Conformance means content parity on the material fields: `type`, `required`, `additionalProperties`, and each property's type and constraints. The top-level `description` may diverge where the methodology adds context appropriate to its own surface. Drift between a vendored schema and its declared canonical is a governance moment handled during review, not a runtime failure.

**Runtime reads from the methodology.** Consumers that read schemas at runtime — runa, agentd, operator tooling — read from whichever methodology is active, never from commons. commons is the design-time authority; the methodology is the runtime surface. This preserves the sovereignty boundary: commons owns authoring, methodologies own runtime.

**What this means for the builder agent:** When proposing a new cross-component artifact type, test it against the canonicalization criteria first. If it qualifies, produce the pair (prose + versioned schema) in commons and cite this ADR; do not produce the schema in a methodology with an intent to promote it later — promotion paths invite drift windows. When adding a vendored copy of a canonical to a methodology, record immutable provenance at the same time; a vendored copy without provenance is a silent divergence waiting to happen.
