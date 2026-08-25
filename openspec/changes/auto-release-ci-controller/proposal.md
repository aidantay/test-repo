## Why

Currently, `release-please` creates Release PRs on main branch pushes, but publishing artifacts (`publish-docs`, `publish-exe`, `publish-docker`) either fails or executes prematurely because release tags are created only when a Release PR is merged. Configuring `release-please.yml` to automatically merge Release PRs and export release outputs enables `ci.yml` to trigger downstream publishing jobs fully automatically upon release creation without manual intervention.

## What Changes

- **Update `release-please.yml`**: Expose `releases_created` and `tag_name` job outputs via `workflow_call`, and add an `Auto-merge Release PR` step using `gh pr merge --auto --merge`.
- **Update `ci.yml`**: Configure `ci.yml` to call `release-please.yml` first and evaluate `if: needs.release.outputs.releases_created == 'true'` before triggering `publish-docs`, `publish-exe`, and `publish-docker`.

## Capabilities

### New Capabilities
- `ci-workflows`: Automated Release PR auto-merging and conditional downstream publishing pipeline.

### Modified Capabilities
<!-- None -->

## Impact

- **Affected Files**: `.github/workflows/ci.yml`, `.github/workflows/release-please.yml`.
- **Automation Impact**: Fully automates release creation and artifact deployment upon push to main.
