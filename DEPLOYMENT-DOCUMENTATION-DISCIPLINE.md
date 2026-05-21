# Deployment Documentation Discipline

*A discipline for documenting a deployment — a host, and the configured
environment running on it. It defines what a deployment's documentation must
contain, what makes that documentation usable rather than merely descriptive,
and how it relates to the shared baseline a host is built from. It is a general
practice: it applies to any deployment and is not a description of any one
host. It is a Day-One artifact — provisional, and refined by what its
application surfaces.*

## 1. Purpose, subject, and what deployment documentation must achieve

**Subject.** A *deployment* is a host — a configured operating environment that
runs services, that is owned and operated, and that something depends on. This
discipline addresses the documentation of a deployment specifically. A codebase
and a shared-convention collection are different kinds of artifact with
different documentation needs; this discipline is not about them.

**Purpose.** The discipline defines how a deployment is documented so that the
documentation is genuinely usable — so that it can be acted on, not merely
read.

**What the documentation must achieve.** A deployment's documentation exists so
that:

- a future operator or agent can operate, recover, and change the host without
  the original author present;
- a future operator or agent can rebuild or re-derive the host from the
  documentation;
- a contributor can orient to the host from the documentation alone;
- the documentation stays true to the host as the host changes.

These are the discipline's ground. Everything below derives from them, and
where the discipline is silent or ambiguous, the resolution is reckoned from
them.

## 2. The content model

A deployment's documentation must let a reader satisfy each of the following.
These are required properties, not a mandated file layout — the host owns how
it organizes and formats them.

- **Identity and scope.** Which host this is. Its purpose — the role it plays
  and why it exists. What its documentation covers and what it does not.
- **Topology.** What runs where: the services, processes, and components on the
  host, and how they relate. The requirement is that the topology is
  recoverable from the documentation; diagram, table, or prose is the host's
  choice.
- **Configuration record.** The host's desired-state configuration — its
  configuration source, version pins, and the relationship between desired and
  observed state — expressed as derivation from the host's baseline (§3).
- **Operations reference.** Who owns the host; how it is reached (access paths,
  not secrets); what it depends on; how it is observed — monitoring, logs,
  alerts.
- **Procedures.** The operational procedures the host needs — at minimum, how
  it is provisioned, how it is recovered, and how a change is applied to it.
  Procedure form is specified below.
- **Change and drift controls.** How changes to the host are made and recorded;
  how drift from desired state is detected; how the documentation is updated
  when the host changes.

**Procedure form.** A procedure in a deployment's documentation is *execution
substrate* — something an operator or agent follows as authority. Each
procedure states: its outcome, what is true when it has succeeded; its
prerequisites; the tools and permissions it requires; its steps; what to do
when a step fails; whom to escalate to; and its owner. A procedure must be
executable by someone who did not write it and does not hold the author's
context.

Because procedures are execution substrate, the Procedure Substrate Discipline
(commons ADR-0013) governs them: when a procedure has a gap, the gap is
substrate work — repaired in the procedure — not a local workaround. A
deployment's procedures must therefore be written concretely enough that "this
procedure has a gap" is a decidable condition.

## 3. The inheritance rule

A host is rarely configured from nothing. Its setup customizes a shared
baseline — a host-setup practice maintained separately and used by more than
one host. The discipline's rule for the relationship between a host's
documentation and its baseline:

**A deployment's documentation does not re-document what its baseline already
documents.** With respect to the baseline, it records three things, and only
these:

1. **Derivation point.** Which baseline the host is built from, and which
   version of it. This is the anchor: a reader knows that everything the
   baseline documents, at that version, applies — except where this document
   explicitly says otherwise.
2. **Customizations.** Each point where the host diverges from the baseline,
   with the reason for the divergence. A customization without a recorded
   reason cannot be told apart from drift.
3. **Host-specific additions.** What this host has that the baseline does not
   address at all — its identity, its purpose, what is deployed on it.

**Host-specific content is kept minimal and justified.** Configuration that
could have lived in the baseline belongs in the baseline. Host-specific entries
are deliberate exceptions, divergences, tests, or genuine single-host concerns
— never arbitrary content. When host-specific content accumulates past genuine
exceptions, that is a signal the baseline should absorb it.

**This rule is also the boundary rule.** It answers what is, and is not, a
given host's deployment documentation: what the baseline documents belongs to
the baseline; what a host customizes or adds belongs to the host. A host's
deployment documentation is its derivation point, its customizations, and its
host-specific additions — and nothing the baseline already carries.

## 4. Applicability

Deployment documentation is *applicable* when an operator or agent can act from
it directly, rather than only learn about the system from it. The discipline
holds documentation to the following properties. Each is a yes/no check —
usable both while producing documentation and while auditing it.

- **Discoverable from the trigger.** A reader who hits an alert, a task, or a
  question can reach the relevant document from the host, the service, or the
  configuration item — without already knowing where it lives.
- **Modes separated.** Executable steps, reference facts, and explanation are
  not interleaved in one passage. A procedure is not broken up by background; a
  reference is not broken up by rationale.
- **Authority explicit.** Owner, version or last-modified date, environment,
  and scope are stated. A reader can tell whether what they are reading is
  current and whom it belongs to.
- **State connected.** Desired state, observed state, and exceptions are linked
  — a reader can tell what the host should be, what it is, and where the two
  deliberately differ.
- **Derivation shown.** The host's relationship to its baseline (§3) is
  visible: derivation point, customizations, host-specific additions.
- **Second-operator executable.** Each procedure can be carried out correctly
  by someone who did not write it.
- **Update responsibility bound.** Each part of the documentation has a defined
  trigger for being updated — a code or configuration change, a
  change-management step, an incident follow-up, or automated regeneration.
  Documentation with no update trigger will drift.

Documentation that fails these properties is descriptive, not applicable.
Auditing existing documentation (§6) is, first of all, running these checks.

## 5. Home and currency

**Home.** A deployment's documentation lives with the substrate it documents —
co-located with the host's own configuration source, in the host's own
repository, under version control. It is not spread across repositories that
own other things, and it is not separated from the configuration it describes.
The shared baseline lives in its own home; a specific host's deployment
documentation lives in that host's own repository.

**Currency.** Documentation that has drifted from the host is worse than no
documentation, because it misleads with the authority of a document. The
discipline keeps documentation current by:

- **Docs-as-code.** The documentation is plain text under version control,
  changed through the same review path as the substrate it describes. A change
  to the host and the change to its documentation land together.
- **Change-management coupling.** When a host changes, updating its
  documentation is part of making the change — not a separate, later, optional
  task.
- **Generated or governed records where possible.** Where a part of the
  documentation can be derived from the host's actual state, deriving it is
  more reliable than maintaining it by hand.

## 6. Applying the discipline

The discipline is used in two ways.

**For a new deployment.** Produce documentation to the content model (§2): each
part present, the inheritance rule (§3) followed, the applicability properties
(§4) satisfied, the result homed and kept current per §5.

**For existing documentation.** Audit it and bring it to standard:

1. Identify the host's deployment documentation, applying the boundary rule
   (§3) to separate it from baseline content and from content that belongs to
   other things.
2. Check it against the content model (§2): which parts are present, which are
   missing, which are mixed with content that does not belong.
3. Check it against the applicability properties (§4): which hold, and which
   fail.
4. Restructure to close the gaps — content moved into the right parts, the
   inheritance rule applied, applicability failures repaired, the result homed
   and current per §5.

**Applying the discipline is itself a procedure**, and the Procedure Substrate
Discipline governs it: if, while applying the discipline, the discipline itself
proves to have a gap — a case it does not cover, a check that cannot be decided
— that gap is substrate work on this discipline, not a local improvisation to
be quietly worked around. The discipline is a Day-One artifact: whatever it
currently is, it is foundation for what its application teaches next.
