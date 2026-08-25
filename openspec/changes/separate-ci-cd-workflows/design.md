## Context

See `proposal.md` for motivation. Currently, `.github/workflows/ci.yml` serves as the central release orchestrator, combining release automation (`release-please.yml`) and documentation deployment (`publish-docs.yml`) without running test suites or CI verification.

## Goals / Non-Goals

**Goals:**
- Create a dedicated reusable `test.yml` sub-workflow executing stage unit test matrices via `workflow_call` or `workflow_dispatch`.
- Update `ci.yml` to trigger `test.yml` on PRs and pushes to `main`.
- Create a dedicated `cd.yml` workflow orchestrating release creation and asset distribution.
- Enforce gating so `cd.yml` only runs after `ci.yml` successfully completes on `main`.
- Activate `publish-docs` in `cd.yml` while leaving `publish-exe` and `publish-docker` defined but commented out for future enablement.

**Non-Goals:**
- Including linting, formatting, or typechecking in `ci.yml` or `test.yml`.
- Modifying the underlying reusable sub-workflows (`release-please.yml`, `publish-docs.yml`, `publish-exe.yml`, `publish-docker.yml`).

## Decisions

### Decision 1: Reusable Sub-workflow Architecture (`test.yml`)
- **Choice**: Encapsulate test matrix execution within `.github/workflows/test.yml`, supporting `workflow_call` and `workflow_dispatch`, matching the repo's existing reusable sub-workflow pattern.
- **Rationale**: Keeps `ci.yml` concise as an orchestrator and allows running test matrices independently via manual dispatch or downstream workflow reuse.

### Decision 2: Gating CD behind CI using GitHub Actions `workflow_run`
- **Choice**: Configure `cd.yml` with `on: workflow_run: workflows: ["CI"], branches: [main], types: [completed]`, checking `if: ${{ github.event.workflow_run.conclusion == 'success' }}`.
- **Rationale**: Guarantees releases and asset deployments never execute if unit tests in `ci.yml` fail.

### Decision 3: Staged Asset Publishing in `cd.yml`
- **Choice**: Wire `release` job to run `release-please.yml`, followed by `publish-docs` dependent on `needs.release.outputs.releases_created == 'true'`. Keep `publish-exe` and `publish-docker` jobs present in `cd.yml` but commented out.

## Risks / Trade-offs

- [Risk: `workflow_run` default branch context] → `workflow_run` triggers in default branch context (`main`). Mitigation: Ensure `cd.yml` explicitly checks `github.event.workflow_run.conclusion == 'success'` before triggering `release-please`.
