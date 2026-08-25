## Purpose

Provides centralized workflow orchestration and reusable sub-workflow dispatch for CI/CD automation across the truetrace project.

## ADDED Requirements

### Requirement: Central CI Controller Workflow Execution

The central CI controller workflow SHALL act as the primary entrypoint for CI/CD workflow execution on repository push, pull request, and manual workflow dispatch events.

#### Scenario: Main branch push pipeline execution
- **WHEN** code is pushed to the `main` branch
- **THEN** the central CI controller workflow executes `release-please.yml` first, and upon completion triggers parallel execution of `publish-docs.yml`, `publish-exe.yml`, and `publish-docker.yml`.

#### Scenario: Sub-workflow reusability via workflow_call
- **WHEN** a sub-workflow (`publish-docs.yml`, `publish-exe.yml`, `publish-docker.yml`, or `release-please.yml`) is invoked by `ci.yml`
- **THEN** the sub-workflow MUST accept `workflow_call` events and execute with inherited repository secrets.
