# Set default goal to display help
.DEFAULT_GOAL := help

# Configure standard shell execution rules
SHELL := /usr/bin/env bash
.SHELLFLAGS := -eu -o pipefail -c

# Suppress entering/leaving directory messages globally
MAKEFLAGS += --no-print-directory

# Define a default registry/username, but allow overriding it via environment or command line
REGISTRY ?=
IMAGE_NAME := test-repo
VERSION := 0.1.2 # x-release-please-version

# Automatically discover stages
STAGES := $(filter-out decode, $(notdir $(wildcard stages/*)))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     MACROS & FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

define CHECK_STAGE
    @if [ -z "$(stage)" ]; then \
        echo "Error: stage cannot be empty. Usage: make $@ stage=<stage_name>"; \
        exit 1; \
    fi
endef

define CHECK_REGISTRY
	@if [ -z "$(REGISTRY)" ]; then \
		echo "Error: REGISTRY cannot be empty. Usage: make $@ REGISTRY=<username>"; \
		exit 1; \
	fi
endef

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     USAGE TARGET
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.PHONY: help clean-all

help: ## Show this help message
	@echo "Usage: make [target] [stage=stage_name]"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

clean-all: clean-venv-all clean-docs-all clean-exe-all
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".venv" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name "uv.lock" -exec rm -rf {} +

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     VENV TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ Venv Targets

.PHONY: clean-venv clean-venv-all \
	build-venv build-venv-all \
	format-venv format-venv-all \
	lint-venv lint-venv-all \
	typecheck-venv typecheck-venv-all \
	test-venv test-venv-all
	check-venv-all

check-venv-all: format-venv-all lint-venv-all typecheck-venv-all test-venv-all

clean-venv: ## Clean a single stage venv (e.g., make clean-venv stage=01-windows)
	$(call CHECK_STAGE)
	@find stages/$(stage) -type d -name "__pycache__" -exec rm -rf {} +
	@find stages/$(stage) -type d -name ".venv" -exec rm -rf {} +
	@find stages/$(stage) -type d -name ".pytest_cache" -exec rm -rf {} +
	@find stages/$(stage) -type d -name ".ruff_cache" -exec rm -rf {} +
	@find stages/$(stage) -type d -name ".mypy_cache" -exec rm -rf {} +
	@find stages/$(stage) -type f -name "uv.lock" -exec rm -rf {} +

clean-venv-all: ## Clean all stages venvs
	@for stage_name in $(STAGES); do \
		echo "Cleaning venv stage: $$stage_name"; \
		$(MAKE) clean-venv stage=$$stage_name; \
	done

build-venv: ## Build a single stage venv (e.g., make build-venv stage=01-windows)
	$(call CHECK_STAGE)
	@uv sync --project stages/$(stage)

build-venv-all: ## Build all stages venvs
	@for stage_name in $(STAGES); do \
		echo "Building venv stage: $$stage_name"; \
		$(MAKE) build-venv stage=$$stage_name; \
	done

format-venv: ## Format a single stage (e.g., make format-venv stage=01-windows)
	$(call CHECK_STAGE)
	@status=0; \
	uv run --project stages/$(stage) --group dev \
		ruff format stages/$(stage) || status=$$?; \
	exit $$status

format-venv-all: ## Format all stages
	@failed=0; \
	for stage_name in $(STAGES); do \
		echo "Formatting stage: $$stage_name"; \
		$(MAKE) format-venv stage=$$stage_name || failed=1; \
	done; \
	exit $$failed

lint-venv: ## Lint a single stage (e.g., make lint-venv stage=01-windows)
	$(call CHECK_STAGE)
	@status=0; \
	uv run --project stages/$(stage) --group dev \
		ruff check stages/$(stage) || status=$$?; \
	exit $$status

lint-venv-all: ## Lint all stages
	@failed=0; \
	for stage_name in $(STAGES); do \
		echo "Linting stage: $$stage_name"; \
		$(MAKE) lint-venv stage=$$stage_name || failed=1; \
	done; \
	exit $$failed

typecheck-venv: ## Typecheck a single stage (e.g., make typecheck-venv stage=01-windows)
	$(call CHECK_STAGE)
	@status=0; \
	uv run --project stages/$(stage) --group dev \
		mypy stages/$(stage) || status=$$?; \
	exit $$status

typecheck-venv-all: ## Typecheck all stages
	@failed=0; \
	for stage_name in $(STAGES); do \
		echo "Typechecking stage: $$stage_name"; \
		$(MAKE) typecheck-venv stage=$$stage_name || failed=1; \
	done; \
	exit $$failed

test-venv: ## Test a single stage (e.g., make test-venv stage=01-windows)
	$(call CHECK_STAGE)
	@failed=0; \
	uv run --project stages/$(stage) --group dev \
		pytest stages/$(stage)/tests || failed=1; \
	exit $$failed

test-venv-all: ## Test all stages
	@failed=0; \
	for stage_name in $(STAGES); do \
		echo "Testing stage: $$stage_name"; \
		$(MAKE) test-venv stage=$$stage_name || failed=1; \
	done; \
	exit $$failed

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     CONTAINER IMAGE TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ Container Image Targets

.PHONY: clean-image clean-image-all \
	build-image build-image-all \
	push-image push-image-all \
	publish-image publish-image-all

publish-image: clean-image build-image push-image

publish-image-all: clean-image-all build-image-all push-image-all

clean-image: ## Clean a single stage container image (e.g., make clean-image stage=01-windows)
	$(call CHECK_REGISTRY)
	$(call CHECK_STAGE)
	@docker rmi $(REGISTRY)/$(IMAGE_NAME)-$(stage):v$(VERSION) || true

clean-image-all: ## Clean all container images
	$(call CHECK_REGISTRY)
	@for stage_name in $(STAGES); do \
		echo "Cleaning image for stage: $$stage_name"; \
		$(MAKE) clean-image stage=$$stage_name; \
	done

build-image: ## Build a single stage container image (e.g., make build-image stage=01-windows)
	$(call CHECK_REGISTRY)
	$(call CHECK_STAGE)
	@docker build \
		-f stages/$(stage)/Dockerfile \
		-t $(REGISTRY)/$(IMAGE_NAME)-$(stage):v$(VERSION) \
		-q \
		.

build-image-all: ## Build all container images
	$(call CHECK_REGISTRY)
	@for stage_name in $(STAGES); do \
		echo "Building image for stage: $$stage_name"; \
		$(MAKE) build-image stage=$$stage_name; \
	done

push-image: ## Push a single stage to Docker Hub (e.g., make push-image stage=01-windows)
	$(call CHECK_REGISTRY)
	$(call CHECK_STAGE)
	@docker push $(REGISTRY)/$(IMAGE_NAME)-$(stage):v$(VERSION)

push-image-all: ## Push all container images to Docker Hub
	$(call CHECK_REGISTRY)
	@for stage_name in $(STAGES); do \
		echo "Pushing image for stage: $$stage_name"; \
		$(MAKE) push-image stage=$$stage_name; \
	done

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     BINARY EXECUTABLE TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ Binary Executable Targets

.PHONY: clean-exe clean-exe-all \
	build-exe build-exe-all

clean-exe: ## Clean executables for a single stage (e.g., make clean-exe stage=01-windows)
	$(call CHECK_STAGE)
	@rm -rf dist/truetrace-$(stage) build/truetrace-$(stage)
	@rm -rf truetrace-$(stage).spec

clean-exe-all: ## Clean all executables
	@for stage_name in $(STAGES); do \
		echo "Cleaning executable for stage: $$stage_name"; \
		$(MAKE) clean-exe stage=$$stage_name; \
	done
	@rm -rf build dist

build-exe: ## Build executable for a single stage (e.g., make build-exe stage=01-windows)
	$(call CHECK_STAGE)
	@main_file=$$(find "stages/$(stage)/src" -name "main.py" 2>/dev/null | head -n 1); \
	if [ -n "$$main_file" ]; then \
		uv run --project stages/$(stage) --group build pyinstaller \
			--clean --noconfirm --log-level ERROR --onefile \
			--specpath build \
			--workpath build \
			--distpath dist \
			--name "truetrace-$(stage)" \
			"$$main_file"; \
	else \
		echo "No main.py found for stage $(stage)"; \
	fi

build-exe-all: ## Build all executables
	@for stage_name in $(STAGES); do \
		echo "Building executable for stage: $$stage_name"; \
		$(MAKE) build-exe stage=$$stage_name; \
	done

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     DOCUMENTATION TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ Documentation Targets

.PHONY: clean-docs clean-docs-all \
	prep-docs prep-docs-all \
	serve-docs build-docs \
	deploy-docs publish-docs

preview-docs: clean-docs-all prep-docs-all serve-docs

deploy-docs: clean-docs-all prep-docs-all build-docs

clean-docs: ## Clean docs for a single stage (e.g., make clean-docs stage=01-windows)
	$(call CHECK_STAGE)
	@rm -rf \
		docs/stages/$(stage).md \
		docs/api/$(stage).md

clean-docs-all: ## Clean all docs
	@for stage_name in $(STAGES); do \
		echo "Cleaning docs for stage: $$stage_name"; \
		$(MAKE) clean-docs stage=$$stage_name; \
	done
	@rm -rf \
		site \
		.cache \
		.venv \
		docs/stages \
		docs/api

prep-docs: ## Prepare docs for a single stage (e.g., make prep-docs stage=01-windows)
	$(call CHECK_STAGE)
	@mkdir -p docs/stages docs/api
	@ln -sf "../../stages/$(stage)/docs/index.md" "docs/stages/$(stage).md"
	@ln -sf "../../stages/$(stage)/docs/api.md" "docs/api/$(stage).md"

prep-docs-all: ## Prepare all docs
	@mkdir -p docs/stages docs/api
	@for stage_name in $(STAGES); do \
		echo "Preparing docs for stage: $$stage_name"; \
		$(MAKE) prep-docs stage=$$stage_name; \
	done
	@ln -sf "../../commons/shared_libs/docs/api.md" "docs/api/shared-libs.md"

serve-docs: ## Serve documentation locally
	@uv run zensical serve

build-docs: ## Build documentation site
	@uv run zensical build
