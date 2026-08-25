## Why

Currently, `ci.yml` serves as the central release orchestrator rather than a true Continuous Integration workflow, causing confusion and mixing pull-request testing logic with release deployment logic. Decoupling CI (testing) from CD (release automation and asset distribution) establishes a clean separation of concerns, improves PR validation speed, and ensures CD releases only execute after CI checks succeed on `main`.

## What Changes

- **Create `test.yml`**: Modular reusable sub-workflow for running stage unit test matrices via `workflow_call` or `workflow_dispatch`.
- **Modify `ci.yml`**: Refactor into a dedicated Continuous Integration workflow triggering on pull requests and pushes to `main` that delegates stage matrix testing to `test.yml`.
- **Create `cd.yml`**: Introduce a dedicated Continuous Delivery & Release Automation workflow triggering when `ci.yml` succeeds on `main`.
- **Decouple Release Orchestration**: Move invocation of `release-please.yml` and asset distribution sub-workflows out of `ci.yml` into `cd.yml`.
- **Stage Distribution Pipelines**: In `cd.yml`, activate `publish-docs.yml` while leaving `publish-exe.yml` and `publish-docker.yml` disabled (commented out) until ready.

## Capabilities

### Modified Capabilities

- `ci-workflows`: Decouple CI test matrix execution into reusable sub-workflow `test.yml` invoked by `ci.yml`, and gate release asset publishing in `cd.yml` on CI completion.

## Impact

- Workflow files: `.github/workflows/ci.yml`, `.github/workflows/cd.yml`, `.github/workflows/test.yml`.
- Reusable workflows: `.github/workflows/test.yml`, `.github/workflows/release-please.yml`, `.github/workflows/publish-docs.yml`, `.github/workflows/publish-exe.yml`, `.github/workflows/publish-docker.yml`.
- Trigger relationships: `ci.yml` calls `test.yml`; `cd.yml` depends on `ci.yml` completion or status on `main`.
