## Why

`release-please` relies on Conventional Commit formatting in commit messages to calculate automated semantic versions and changelogs. Adding commitlint validation with a dedicated configuration file (`.commitlintrc.json`) directly into the `CI` workflow (`ci.yml`) ensures all commit messages in PR branches conform to Conventional Commits standards.

## What Changes

- **Create `.commitlintrc.json`**: Add conventional commit linting rules extending `@commitlint/config-conventional`.
- **Modify `ci.yml`**: Add permissions for `contents: read` / `pull-requests: read` and introduce a `commitlint` job using `wagoid/commitlint-github-action@v6` conditioned on `pull_request` events.

## Capabilities

### Modified Capabilities

- `ci-workflows`: Add commit message validation against `.commitlintrc.json` to the `ci.yml` workflow for Pull Requests targeting `main`.

## Impact

- Repository files: `.commitlintrc.json`, `.github/workflows/ci.yml`.
- Pull Requests: Block merging of PRs with commit messages that do not follow Conventional Commits standard.
