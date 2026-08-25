## Why

The current GitHub Actions workflows in `.github/workflows/` (publish-docs, publish-exe, publish-docker, release-please) are triggered individually via manual `workflow_dispatch` or isolated push triggers, lacking unified orchestration and sequential execution. Centralizing workflow orchestration into a primary `ci.yml` controller ensures that releases, builds, and publishing happen in a structured, programmatic, and maintainable order.

## What Changes

- **Add `ci.yml` Controller Workflow**: Introduce a new central workflow (`.github/workflows/ci.yml`) acting as the single entrypoint for CI/CD pipeline execution on `push`, `pull_request`, and `workflow_dispatch`.
- **Refactor Sub-Workflows to Reusable (`on: workflow_call`)**: Update existing workflows (`publish-docs.yml`, `publish-exe.yml`, `publish-docker.yml`, `release-please.yml`) to accept `on: workflow_call` so they can be invoked programmatically by `ci.yml`.
- **Enforce Sequential Pipeline Execution**: Configure `ci.yml` to trigger `release-please` first on push to main, followed by parallel execution of `publish-docs`, `publish-exe`, and `publish-docker`.

## Capabilities

### New Capabilities
- `ci-workflows`: Centralized CI/CD workflow orchestration and reusable sub-workflow dispatch for the `truetrace` project.

### Modified Capabilities
<!-- None -->

## Impact

- **Affected Files**: `.github/workflows/ci.yml` (new), `.github/workflows/publish-docs.yml`, `.github/workflows/publish-exe.yml`, `.github/workflows/publish-docker.yml`, `.github/workflows/release-please.yml`.
- **CI/CD Execution**: Standardizes automated release and artifact publishing flow. `mirror.yml` remains untouched for now.
