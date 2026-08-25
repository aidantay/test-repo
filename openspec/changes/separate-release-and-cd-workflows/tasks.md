## 1. Create Release Workflow

- [x] 1.1 Create `.github/workflows/release.yml` triggering on `workflow_run` of `CI` (`branches: [main]`) and `workflow_dispatch`
- [x] 1.2 Embed `release-please` actions directly in `release.yml` and remove `.github/workflows/release-please.yml`

## 2. Refactor CD Workflow

- [x] 2.1 Update `.github/workflows/cd.yml` trigger to `on: release` (`types: [published]`) and `on: push` (`tags: ['v*']`)
- [x] 2.2 Remove `release` job from `cd.yml`
- [x] 2.3 Update downstream publishing jobs (`publish-image`, `deploy-docs`, `publish-exe`) in `cd.yml` to run without `needs: release` condition

## 3. Update Publishing Workflows

- [x] 3.1 Update `.github/workflows/publish-image.yml` to use tag parameter or default `ref` for `actions/checkout`
- [x] 3.2 Ensure `make build-docker` and `make push-docker` in `publish-image.yml` handle tag/version passing cleanly

## 4. Verification

- [x] 4.1 Validate workflow syntax across `.github/workflows/release.yml`, `.github/workflows/cd.yml`, and `.github/workflows/publish-image.yml`
