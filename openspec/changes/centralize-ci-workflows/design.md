## Context

See `proposal.md` for motivation.

The project currently has individual workflow files under `.github/workflows/`:
- `publish-docs.yml`
- `publish-exe.yml`
- `publish-docker.yml`
- `release-please.yml`
- `mirror.yml`

Currently, these workflows use standalone `workflow_dispatch` triggers or push triggers, operating independently.

## Goals / Non-Goals

**Goals:**
- Create `.github/workflows/ci.yml` to orchestrate workflow execution centrally.
- Update existing workflows (`publish-docs.yml`, `publish-exe.yml`, `publish-docker.yml`, `release-please.yml`) to support `on: workflow_call`.
- Enforce release-first order: `release-please` creates release tags and updates `CHANGELOG.md` before publishing docs or build artifacts.

**Non-Goals:**
- Modifying `mirror.yml` in this change.
- Adding unit test or lint execution stages in this change.
- Changing `Makefile` build targets.

## Decisions

### Decision 1: Reusable Workflows (`on: workflow_call`) over API Dispatcher or Process Scripts
- **Choice**: Convert existing `.yml` workflows to reusable workflows triggered via `uses: ./.github/workflows/<file>.yml` in `ci.yml`.
- **Rationale**: Keeps native GitHub UI job status reporting, matrix progress, logs, and failure reporting clean without requiring custom GitHub App tokens or script overhead.
- **Alternatives Considered**: Custom API dispatch script via `gh workflow run` (adds PAT requirement and splits job logs).

### Decision 2: Sequential Pipeline DAG (`release` -> [`publish-docs`, `publish-exe`, `publish-docker`])
- **Choice**: Execute `release-please` first, followed by parallel execution of `publish-docs`, `publish-exe`, and `publish-docker` using `needs: release`.
- **Rationale**: `publish-exe.yml` uploads assets to a GitHub Release and `publish-docs.yml` renders the documentation site. Running `release-please` first ensures version tags and updated `CHANGELOG.md` are available to downstream publishing steps.

## Risks / Trade-offs

- **[Risk] Secrets forwarding to reusable workflows** → **Mitigation**: Specify `secrets: inherit` in `ci.yml` for all called jobs.
- **[Risk] Multiple `on:` triggers conflicting in sub-workflows** → **Mitigation**: Retain `workflow_dispatch` alongside `workflow_call` in sub-workflows to preserve manual fallback capability.
