# commons

Shared principles and standards for the Tesserine ecosystem.

## What this is

This repo holds the bedrock principles, design principles, and architectural decision records (ADRs) that define standards across all Tesserine components. Every repo — whether it builds infrastructure, runtime, or methodology — derives its standards from what lives here.

## Ecosystem repos

- **[agentd](https://github.com/tesserine/agentd)** — container lifecycle daemon for autonomous agent sessions
- **[runa](https://github.com/tesserine/runa)** — cognitive runtime enforcing methodology topologies
- **[groundwork](https://github.com/tesserine/groundwork)** — contributor methodology plugin (first methodology)
- **[base](https://github.com/tesserine/base)** — reference container image for agent sessions

Future repos inherit these principles by default.

## Contents

- **[PRINCIPLES.md](PRINCIPLES.md)** — seven bedrock principles organized as a topology (sovereignty, sequence, grounding, obligation to dissent, recursive improvement, transmission, verifiable completion)
- **[DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md)** — sixteen engineering judgment principles governing how we think about code (elimination over accommodation, fix at the source, honest naming, correctness over optimization, architecture as communication, review discipline)
- **[EXIT-CODES.md](EXIT-CODES.md)** — shared session-outcome exit code contract for runners and callers across the ecosystem
- **[adr/](adr/)** — architectural decision records that operationalize the principles

## Relationship to individual repos

Each repo may have its own repo-specific ADRs that trace back to the shared principles defined here. This repo holds what is universal across the ecosystem; individual repos hold what is specific to their domain.

## Proposing changes

Open an issue or pull request on this repo. Changes to shared principles affect the entire ecosystem, so proposals should demonstrate that the change serves the ecosystem's trajectory, not just one repo's convenience.
