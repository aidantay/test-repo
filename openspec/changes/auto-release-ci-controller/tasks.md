## 1. Release Workflow Enhancements

- [x] 1.1 Update `.github/workflows/release-please.yml` to define `workflow_call` outputs for `releases_created` and `tag_name`.
- [x] 1.2 Add `Auto-merge Release PR` step to `.github/workflows/release-please.yml` using `gh pr merge --auto --merge`.
- [x] 1.3 Pass token secrets (`secrets.RELEASE_PAT || secrets.GITHUB_TOKEN`) to release-please action and gh CLI merge step.

## 2. Central Controller Workflow Updates

- [x] 2.1 Update `.github/workflows/ci.yml` to pass outputs from `release` job to downstream jobs.
- [x] 2.2 Configure `publish-docs`, `publish-exe`, and `publish-docker` jobs in `ci.yml` with `if: ${{ needs.release.outputs.releases_created == 'true' }}` and pass `tag`.

## 3. Verification

- [x] 3.1 Validate YAML syntax across `.github/workflows/release-please.yml` and `.github/workflows/ci.yml`.
