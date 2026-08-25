## Purpose

Provides Continuous Integration (CI) test execution and Continuous Delivery (CD) release automation workflows for the truetrace repository.

## ADDED Requirements

### Requirement: Decoupled Reusable CI Test Execution
The Continuous Integration workflow (`ci.yml`) SHALL trigger test execution by delegating to a modular reusable sub-workflow (`test.yml`) on pull request and main branch push events, without executing release or non-test tasks.

#### Scenario: Pull request stage matrix testing via sub-workflow
- **WHEN** code is pushed or a pull request is opened/updated targeting `main`
- **THEN** `ci.yml` invokes `test.yml` via `workflow_call`, which executes `make test-venv` for each stage in a matrix strategy without running linting, formatting, or typechecking checks.

### Requirement: Gated CD Release Automation
The Continuous Delivery workflow (`cd.yml`) SHALL trigger release automation and asset distribution only after `ci.yml` successfully completes on `main`.

#### Scenario: Release execution post-CI success
- **WHEN** the `CI` workflow (`ci.yml`) completes successfully on the `main` branch
- **THEN** `cd.yml` executes `release-please.yml` to process releases and create version tags.

### Requirement: Staged Production Asset Distribution
The Continuous Delivery workflow (`cd.yml`) SHALL deploy active production assets upon release creation while maintaining staged structure for deferred asset distribution pipelines.

#### Scenario: Active asset deployment on release
- **WHEN** a release tag is created by `release-please.yml`
- **THEN** `cd.yml` triggers `publish-docs.yml` to publish documentation to GitHub Pages, while `publish-exe.yml` and `publish-docker.yml` remain defined but disabled (commented out).
