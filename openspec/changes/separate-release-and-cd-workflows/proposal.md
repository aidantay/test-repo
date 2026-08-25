## Why

Currently, `cd.yml` combines release tag creation (`release-please`) and downstream asset publishing (`publish-image`, `deploy-docs`) in a single workflow run. When `cd.yml` is triggered by `CI` completion, `actions/checkout` checks out the commit that triggered the workflow run (`0.1.11`) rather than the release tag created during the run (`v0.1.12`). Decoupling release creation into a consolidated `release.yml` workflow and triggering `cd.yml` on release/tag publication ensures downstream packaging and publishing jobs naturally check out the published release tag and build assets with the exact release version.

## What Changes

- **Create `release.yml`**: A consolidated workflow triggering on `workflow_run` (after `CI` succeeds on `main`) or `workflow_dispatch` that embeds `release-please-action` directly to process releases, auto-merge release PRs, and generate version tags.
- **Remove `release-please.yml`**: Remove the redundant sub-workflow since release logic is now embedded directly in `release.yml`.
- **Modify `cd.yml`**: Refactor `cd.yml` to trigger on GitHub releases (`types: [published]`) or tag pushes (`tags: ['v*']`) instead of `workflow_run` of `CI`. Remove the `release` job from `cd.yml` and keep downstream publishing jobs (`publish-image`, `deploy-docs`, `publish-exe`).
- **Modify `publish-image.yml`**: Ensure `actions/checkout` checks out `inputs.tag` / `github.ref` and passes version arguments to Docker build/push commands cleanly.

## Capabilities

### Modified Capabilities

- `ci-workflows`: Decouple release tag automation into a consolidated `release.yml` workflow, and re-target `cd.yml` to trigger directly on release publication events so that publishing jobs check out the published tag version.

## Impact

- Workflow files: `.github/workflows/release.yml`, `.github/workflows/cd.yml`, `.github/workflows/publish-image.yml`.
- Removed files: `.github/workflows/release-please.yml`.
- Event flow: `ci.yml` completion -> `release.yml` execution -> Git tag/Release creation -> `cd.yml` execution on tag commit.
