# governance

Shared principles and governance for the pentaxis93 ecosystem.

## What this is

This repo holds the bedrock principles, design principles, and architectural decision records (ADRs) that govern all pentaxis93 projects. Every ecosystem repo — whether it builds infrastructure, runtime, or methodology — derives its standards from what lives here.

## Governed repos

- **[agentd](https://github.com/pentaxis93/agentd)** — the daemon providing infrastructure
- **[runa](https://github.com/pentaxis93/runa)** — the cognitive runtime for contract enforcement and artifact tracking
- **[groundwork](https://github.com/pentaxis93/groundwork)** — the first methodology plugin

Future pentaxis93 repos inherit these principles by default.

## Contents

- **[PRINCIPLES.md](PRINCIPLES.md)** — seven bedrock principles organized as a topology (sovereignty, sequence, grounding, obligation to dissent, recursive improvement, transmission, verifiable completion)
- **[DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md)** — sixteen engineering judgment principles governing how we think about code (elimination over accommodation, fix at the source, honest naming, correctness over optimization, architecture as communication, review discipline)
- **[adr/](adr/)** — architectural decision records that operationalize the principles

## Relationship to individual repos

Each repo may have its own repo-specific ADRs that trace back to the shared principles defined here. This repo holds what is universal across the ecosystem; individual repos hold what is specific to their domain.

## Proposing changes

Open an issue or pull request on this repo. Changes to shared principles affect the entire ecosystem, so proposals should demonstrate that the change serves the ecosystem's trajectory, not just one repo's convenience.
