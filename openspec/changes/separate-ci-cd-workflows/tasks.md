## 1. Refactor Continuous Integration (`ci.yml` & `test.yml`)

- [x] 1.1 Create reusable `.github/workflows/test.yml` running matrix stage testing (`make test-venv stage=${{ matrix.stage }}`) with `workflow_call` and `workflow_dispatch`.
- [x] 1.2 Update `.github/workflows/ci.yml` triggers for `pull_request` and `push` to `main` to invoke `test.yml`.
- [x] 1.3 Ensure `ci.yml` and `test.yml` omit linting, formatting, and typechecking tasks.

## 2. Implement Continuous Delivery & Release Automation (`cd.yml`)

- [x] 2.1 Create `.github/workflows/cd.yml` triggered via `workflow_run` on `CI` workflow completion on `main` branch.
- [x] 2.2 Configure `release` job in `cd.yml` to invoke `./.github/workflows/release-please.yml`.
- [x] 2.3 Configure `publish-docs` job in `cd.yml` to invoke `./.github/workflows/publish-docs.yml` when a new release tag is created.
- [x] 2.4 Add staged `publish-exe` and `publish-docker` jobs to `cd.yml` in a commented-out state.

## 3. Workflow Verification

- [x] 3.1 Verify YAML syntax for `.github/workflows/ci.yml`, `.github/workflows/test.yml`, and `.github/workflows/cd.yml`.
