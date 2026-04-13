# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added `EXIT-CODES.md`, defining the shared session-outcome exit code
  convention for runners and callers, including survey findings, reserved
  POSIX ranges, caller/runner guidance, and forward-compatibility rules.

### Changed

- Renamed repo identity from "governance" to "commons" in README. Updated
  all ecosystem repo links from pentaxis93 to tesserine org. Added base repo
  to the ecosystem listing.

## [0.1.0] — 2026-04-10

First release. Commons defines the shared principles and architectural
decisions that govern all Tesserine ecosystem components.

### Principles

- Seven bedrock principles organized as a topology: sovereignty, sequence,
  grounding, obligation to dissent, recursive improvement, transmission,
  verifiable completion.
- Sixteen engineering design principles governing how code decisions are made
  across the ecosystem: elimination over accommodation, fix at the source,
  honest naming, correctness over optimization, architecture as communication,
  review discipline, and others.

### Architectural decision records

- ADR-0001: Sovereignty — operator owns WHAT, runtime owns HOW.
- ADR-0002: Everything earns its place — no artifact or abstraction persists
  without demonstrated need.
- ADR-0003: Unconditional responsibility — every component owns its failure
  modes without blaming callers.
- ADR-0004: Compound improvement — every operation refines both the object
  and the process.
