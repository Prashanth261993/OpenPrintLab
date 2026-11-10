---
artifact: constitution
status: active
updated: 2026-11-10
---

# OpenPrintLab - bounded optional CAD constraints

This records the user's explicit T-05 approval **before experimental code**.
It does not retroactively claim a constitution governed the existing V1 build.
The user subsequently approved milestone 003's optional CadQuery backend,
bounded generators and own-assistant preview journey (D-02). That approval
precedes 003 implementation and does not authorize migration or paid providers.

## What this project is

A no-key local model catalog, with one approved isolated CadQuery reuse experiment.
User choice: "Start the isolated CadQuery experiment (Recommended)" after being
shown Python/CadQuery, editable rounded trays, STEP/STL and Windows/Linux checks.

## Stack and constraints

Python 3.12 for the experiment, pinned CadQuery in
`experiments/cadquery/.venv`, standard-library unittest, no datastore or service.
The original Python 3.11+ baseline and its optional MCP environment are untouched.
Linux evidence comes from an isolated GitHub Actions job.

## Quality bar

Meet plan.md G-2 dimensions/volume/solid checks, preserve exact baseline artifacts,
record packages, licenses and hashes, and keep physical/slicer evidence false.

## Conventions

Explicit mm parameters, finite/range/relationship validation, no silent repair,
original editable source and exports licensed CC BY 4.0; test/tool code MIT.

## Security baseline

No paid calls, credentials, editor bridges, printer commands or machine G-code.
Install only the experiment dependency closure in the experiment environment.

## Out of bounds

No general CAD engine, default catalog migration, provider integration, T-06,
automatic promotion or physical-testing claim.
Milestone 003 may add a separate optional backend and variant viewer under its
own plan; it must retain the original no-dependency behavior.

## Definition of done

T-05 tests pass on Windows and Linux; STEP/STL and reproducible commands are
available; an evidence-backed choose/decline report states unresolved limits.
Choosing a candidate for a future adapter is not permission to adopt it.
