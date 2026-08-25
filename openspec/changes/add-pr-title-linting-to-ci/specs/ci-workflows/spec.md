## Purpose

Provides Continuous Integration (CI) test execution, PR validation, release tag generation, and Continuous Delivery (CD) asset distribution workflows for the repository.

## ADDED Requirements

### Requirement: Commit Message Semantic Validation
The Continuous Integration workflow (`ci.yml`) SHALL validate that all commit messages in a Pull Request conform to the Conventional Commits specification configured in `.commitlintrc.json` prior to allowing PR merge.

#### Scenario: Valid commit messages
- **WHEN** a Pull Request contains commit messages adhering to Conventional Commits (e.g., `feat(stage): add stage target`)
- **THEN** the `commitlint` job in `ci.yml` passes successfully.

#### Scenario: Invalid commit messages
- **WHEN** a Pull Request contains a commit message that does not follow Conventional Commits (e.g., `wip fix`)
- **THEN** the `commitlint` job in `ci.yml` fails and blocks the PR check.
