## 1. Sub-Workflow Reusability Updates

- [x] 1.1 Update `.github/workflows/release-please.yml` to accept `on: workflow_call`.
- [x] 1.2 Update `.github/workflows/publish-docs.yml` to accept `on: workflow_call`.
- [x] 1.3 Update `.github/workflows/publish-exe.yml` to accept `on: workflow_call`.
- [x] 1.4 Update `.github/workflows/publish-docker.yml` to accept `on: workflow_call`.

## 2. Central Controller Workflow Implementation

- [x] 2.1 Create `.github/workflows/ci.yml` defining triggers for `push`, `pull_request`, and `workflow_dispatch`.
- [x] 2.2 Configure `release` job in `ci.yml` calling `release-please.yml` on `main` branch push.
- [x] 2.3 Configure `publish-docs`, `publish-exe`, and `publish-docker` jobs in `ci.yml` to run in parallel post-release with `secrets: inherit`.

## 3. Verification

- [x] 3.1 Verify YAML syntax across all `.github/workflows/` files.
