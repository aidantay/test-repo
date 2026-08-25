## Purpose

Provides centralized workflow orchestration, release auto-merging, and conditional sub-workflow dispatch for CI/CD automation across the truetrace project.

## ADDED Requirements

### Requirement: Automated Release PR Merging and Outputs

The release-please workflow SHALL export release creation outputs and automatically merge pending Release PRs opened by release-please.

#### Scenario: Auto-merging Release PR
- **WHEN** release-please creates or updates a Release PR
- **THEN** the workflow automatically attempts to merge the Release PR using `gh pr merge --auto --merge`.

#### Scenario: Exporting release outputs
- **WHEN** release-please creates a new release tag
- **THEN** `release-please.yml` MUST export `releases_created` and `tag_name` as job outputs to caller workflows.

### Requirement: Conditional Downstream Artifact Publishing

The central CI controller workflow SHALL invoke downstream publishing sub-workflows only after a release tag has been created.

#### Scenario: Publishing artifacts post-release
- **WHEN** `releases_created` is `true`
- **THEN** `ci.yml` executes `publish-docs`, `publish-exe`, and `publish-docker` in parallel, passing the created release tag to sub-workflows.
