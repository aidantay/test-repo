## Context

See `proposal.md` for motivation.

The project currently has `.github/workflows/ci.yml` orchestrating calls to `release-please.yml`, `publish-docs.yml`, `publish-exe.yml`, and `publish-docker.yml`. However, `release-please` creates Release PRs which must be merged before Git tags exist.

## Goals / Non-Goals

**Goals:**
- Update `release-please.yml` to define `workflow_call` outputs (`releases_created`, `tag_name`) and add auto-merge execution.
- Update `ci.yml` to call `release-please.yml` and check `if: needs.release.outputs.releases_created == 'true'` before running `publish-docs`, `publish-exe`, and `publish-docker`.

**Non-Goals:**
- Creating extra workflow files (maintaining single orchestrator `ci.yml`).
- Modifying `mirror.yml`.

## Decisions

### Decision 1: Auto-Merge Step inside `release-please.yml`
- **Choice**: Use GitHub CLI `gh pr merge ${{ fromJson(steps.release.outputs.pr).number }} --merge --auto` inside `release-please.yml`.
- **Rationale**: Auto-merges Release PRs opened by `release-please` so the subsequent push triggers tag creation without requiring manual PR approval.

### Decision 2: Output Exporting from Reusable `release-please.yml`
- **Choice**: Forward `steps.release.outputs.releases_created` and `steps.release.outputs.tag_name` out of `release-please.yml` via `jobs.release-please.outputs` and `on.workflow_call.outputs`.
- **Rationale**: Allows `ci.yml` to evaluate whether a release tag was created before attempting to attach binary assets or publish docs.

## Risks / Trade-offs

- **[Risk] GitHub GITHUB_TOKEN restriction on cascading events** → **Mitigation**: Use `secrets.RELEASE_PAT || secrets.GITHUB_TOKEN` so PR merges trigger downstream tagging workflows.
- **[Risk] Repo auto-merge settings disabled** → **Mitigation**: Document requirement to enable "Allow auto-merge" and "Allow GitHub Actions to create and approve PRs" in GitHub repository settings.
