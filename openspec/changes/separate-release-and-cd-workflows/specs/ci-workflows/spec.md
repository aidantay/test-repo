## Purpose

Provides Continuous Integration (CI) test execution, release tag generation, and Continuous Delivery (CD) asset distribution workflows for the repository.

## ADDED Requirements

### Requirement: Decoupled Release Generation Workflow
The repository SHALL execute release tag and changelog creation via a single consolidated release workflow (`release.yml`) triggered upon success of `ci.yml` on the main branch, embedding `release-please` actions directly without calling a separate sub-workflow.

#### Scenario: Release workflow execution post-CI success
- **WHEN** the `CI` workflow (`ci.yml`) completes successfully on the `main` branch
- **THEN** `release.yml` executes `release-please` steps to process releases, merge release PRs, and generate version tags.

### Requirement: Release-Driven Asset Distribution Workflow
The Continuous Delivery workflow (`cd.yml`) SHALL trigger downstream publishing jobs (`publish-image`, `deploy-docs`, `publish-exe`) directly on GitHub release publication or release tag pushes.

#### Scenario: Downstream publishing triggered by published release tag
- **WHEN** a release tag (e.g. `v0.1.12`) or GitHub release is published
- **THEN** `cd.yml` triggers downstream publishing workflows, checking out the published release tag commit and building release artifacts with the exact release version.
