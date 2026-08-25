## Context

See proposal.md for motivation.

Currently, `.github/workflows/cd.yml` triggers on `workflow_run` (after `CI` finishes on `main`), running `release-please` first and then downstream jobs `publish-image` and `deploy-docs`. Because `cd.yml` was triggered before the release tag was pushed, `actions/checkout` checks out `github.sha` (version `0.1.11`), resulting in container images tagged with the old version.

## Goals / Non-Goals

**Goals:**
- Consolidate release tag creation into a single `.github/workflows/release.yml` workflow and remove `.github/workflows/release-please.yml`.
- Reconfigure `.github/workflows/cd.yml` to trigger on published GitHub releases (`release: types [published]`) or tag pushes (`push: tags ['v*']`).
- Update `publish-image.yml` to check out the tag ref and use `inputs.tag` or tag version cleanly.

**Non-Goals:**
- Changing `release-please` config (`.release-please-config.json`).
- Modifying stage Dockerfiles or build scripts in `Makefile`.

## Decisions

### Decision 1: Create consolidated `release.yml` triggered on `workflow_run` of `CI`
- **Rationale**: `release.yml` embeds `release-please-action` directly to handle version bumping, changelog creation, PR merging, and Git tag publication in one place, removing the need for a separate `.github/workflows/release-please.yml` sub-workflow.
- **Alternatives Considered**: Keeping a separate `release-please.yml` sub-workflow called by `release.yml`. Rejected to reduce workflow file fragmentation.

### Decision 2: Trigger `cd.yml` on `release: types [published]` or `push: tags ['v*']`
- **Rationale**: Downstream asset publishing should only occur when a release actually exists. Triggering on release/tag publication ensures `actions/checkout` natively checks out the release tag commit containing updated version strings in `Makefile` and `pyproject.toml`.

### Decision 3: Update `publish-image.yml` checkout and inputs
- **Rationale**: `publish-image.yml` should accept `inputs.tag` and pass it to Docker build/push commands or default to `github.ref_name`.

## Risks / Trade-offs

- [Risk] GitHub default `GITHUB_TOKEN` does not trigger workflow runs when creating tags → **Mitigation**: `release.yml` uses `RELEASE_PAT` (`secrets.RELEASE_PAT || secrets.GITHUB_TOKEN`), ensuring tag creation triggers the downstream `cd.yml` workflow.
