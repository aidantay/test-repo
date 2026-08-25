## 1. Commitlint Configuration

- [x] 1.1 Create `.commitlintrc.json` configured to extend `@commitlint/config-conventional`

## 2. CI Workflow Update

- [x] 2.1 Add `commitlint` job to `.github/workflows/ci.yml` using `wagoid/commitlint-github-action@v6` with `actions/checkout@v7` (`fetch-depth: 0`) conditioned on `github.event_name == 'pull_request'`

## 3. Verification

- [x] 3.1 Validate `.commitlintrc.json` format and `.github/workflows/ci.yml` YAML syntax
