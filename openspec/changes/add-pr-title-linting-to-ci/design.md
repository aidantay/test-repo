## Context

See proposal.md for motivation.

`ci.yml` is the primary Continuous Integration entry point triggering on `pull_request` and `push` to `main`. Adding `.commitlintrc.json` allows defining project-wide commit conventions used by commitlint.

## Goals / Non-Goals

**Goals:**
- Create `.commitlintrc.json` configured with `@commitlint/config-conventional`.
- Add a `commitlint` job to `ci.yml` using `wagoid/commitlint-github-action@v6`.
- Gate execution so commitlint runs on `pull_request` events with full checkout history (`fetch-depth: 0`).

**Non-Goals:**
- Modifying `test.yml` or downstream CD workflows (`release.yml`, `cd.yml`).

## Decisions

### Decision 1: Create `.commitlintrc.json` using Conventional Commits configuration
- **Rationale**: Providing `.commitlintrc.json` establishes explicit repository rules for commitlint and allows future customization of allowed scopes or types.

### Decision 2: Use `wagoid/commitlint-github-action@v6` in `ci.yml`
- **Rationale**: `wagoid/commitlint-github-action` automatically reads `.commitlintrc.json` and lints all commits in the PR branch.

## Risks / Trade-offs

- [Risk] Developers pushing intermediate WIP commits will have PR checks fail → **Mitigation**: Developers can amend/rebase commits or squash before pushing to pass commitlint checks.
