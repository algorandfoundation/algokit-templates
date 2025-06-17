.PHONY: help
help: ## Display this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk -F '##' '/^[a-zA-Z_-]+:.*?##/ { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

clean-examples: ## Remove example directories. Optional: use 'id=<example-id>' to remove specific example
	$(if $(id),\
		rm -rf examples/$(id) && echo "Removed example: $(id)",\
		find examples/ -mindepth 1 -type d -exec rm -rf {} + && echo "Removed all examples")

create-examples: ## Create example projects. Optional: use 'id=<example-id>' to create specific example, 'bootstrap=true' to bootstrap projects
	uv run python ./scripts/create_examples.py $(if $(id),--example_id=$(id),) $(if $(bootstrap),--bootstrap=$(bootstrap),)

bootstrap-examples: ## Bootstrap existing example projects. Optional: use 'id=<example-id>' to bootstrap specific example
	uv run python ./scripts/bootstrap_examples.py $(if $(id),--example_id=$(id),)

generate-new-examples: ## Generate new examples by cleaning, creating, and bootstrapping in sequence. Optional: use 'id=<example-id>' to generate specific example
	make clean-examples $(if $(id),id=$(id),)
	make create-examples $(if $(id),id=$(id),)
	make bootstrap-examples $(if $(id),id=$(id),)

validate-example-configuration: ## Validate the examples.yml configuration file
	uv run python ./scripts/validate_configuration.py

push-example: ## Push example to a GitHub branch. Required: 'id=<example-id>'. Optional: 'branch-prefix=<prefix>' (defaults to 'examples')
	@if [ -z "$(id)" ]; then \
		echo "Error: 'id' parameter is required. Use 'make push-example id=<example-id>'"; \
		exit 1; \
	fi
	@if [ ! -d "examples/$(id)" ]; then \
		echo "Error: example directory 'examples/$(id)' does not exist"; \
		exit 1; \
	fi
	@branch_prefix=$${branch_prefix:-examples}; \
	original_branch=$$(git rev-parse --abbrev-ref HEAD); \
	if git show-ref --quiet refs/heads/$$branch_prefix/$(id) || git ls-remote --exit-code --heads origin $$branch_prefix/$(id) > /dev/null; then \
		read -p "Branch $$branch_prefix/$(id) already exists locally or remotely. Delete it? [y/N] " confirm; \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			current_branch=$$(git rev-parse --abbrev-ref HEAD); \
			if [ "$$current_branch" = "$$branch_prefix/$(id)" ]; then \
				git checkout main; \
			fi; \
			git branch -D $$branch_prefix/$(id) 2>/dev/null && echo "Deleted local branch $$branch_prefix/$(id)" || echo "No local branch $$branch_prefix/$(id) to delete"; \
			git push origin --delete $$branch_prefix/$(id) 2>/dev/null && echo "Deleted remote branch $$branch_prefix/$(id)" || echo "No remote branch $$branch_prefix/$(id) to delete"; \
		else \
			echo "Operation cancelled"; \
			exit 1; \
		fi; \
	fi; \
	git checkout -b $$branch_prefix/$(id); \
	mkdir -p /tmp/example-$(id); \
	cp -a examples/$(id)/. /tmp/example-$(id)/; \
	git rm -rf .; \
	cp -a /tmp/example-$(id)/. .; \
	rm -rf /tmp/example-$(id); \
	git add .; \
	git commit -m "Example $(id) with contents at root"; \
	git push -u origin $$branch_prefix/$(id); \
	git checkout $$original_branch; \
	echo "Pushed example to branch $$branch_prefix/$(id) and returned to branch $$original_branch"

create-codespace: ## Create a branch with example files at top level and open a codespace. Required: 'id=<example-id>'
	@if [ -z "$(id)" ]; then \
		echo "Error: 'id' parameter is required. Use 'make create-codespace id=<example-id>'"; \
		exit 1; \
	fi
	@if [ ! -d "examples/$(id)" ]; then \
		echo "Error: example directory 'examples/$(id)' does not exist"; \
		exit 1; \
	fi
	@original_branch=$$(git rev-parse --abbrev-ref HEAD); \
	if git show-ref --quiet refs/heads/tmp/$(id) || git ls-remote --exit-code --heads origin tmp/$(id) > /dev/null; then \
		read -p "Branch tmp/$(id) already exists locally or remotely. Delete it? [y/N] " confirm; \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			current_branch=$$(git rev-parse --abbrev-ref HEAD); \
			if [ "$$current_branch" = "tmp/$(id)" ]; then \
				git checkout main; \
			fi; \
			git branch -D tmp/$(id) 2>/dev/null && echo "Deleted local branch tmp/$(id)" || echo "No local branch tmp/$(id) to delete"; \
			git push origin --delete tmp/$(id) 2>/dev/null && echo "Deleted remote branch tmp/$(id)" || echo "No remote branch tmp/$(id) to delete"; \
		else \
			echo "Operation cancelled"; \
			exit 1; \
		fi; \
	fi; \
	git checkout -b tmp/$(id); \
	mkdir -p /tmp/example-$(id); \
	cp -a examples/$(id)/. /tmp/example-$(id)/; \
	git rm -rf .; \
	cp -a /tmp/example-$(id)/. .; \
	rm -rf /tmp/example-$(id); \
	git add .; \
	git commit -m "Temporary branch for $(id) example with contents at root"; \
	git push -u origin tmp/$(id); \
	gh codespace create -b tmp/$(id); \
	git checkout $$original_branch; \
	echo "Returned to branch $$original_branch"


test-examples: ## Test all examples
	uv run pytest ./scripts/test_examples.py
