PYTHON3=python3
PYLINT=pylint
PIPENV=pipenv
SHELL=sh



all: run

# runner
#===============================================================
init: ## Initial configuration of local environment.
	sh ./bin/scripts/plugin.sh
	pre-commit install
	pip install pipenv
	pipenv sync

run: ## Run this program.
	@${PYTHON3} main.py



# configure
#===============================================================
.PHONY: lint-config-file
lint-config-file: ## Set pylint configuration file.
	${PYLINT} --generate-rcfile > .pylintrc

.PHONY: pip-install
pip-install: ## Configure lockfile based on Pipfile.
	${PIPENV} install

.PHONY: pip-sync
pip-sync: ## Set up your local environment based on the lock file.
	${PIPENV} sync

.PHONY: pip-update
pip-update: ## Update the package to the latest.
	${PIPENV} update



# Makefile config
#===============================================================
help: ## Display this help screen
	echo "Usage: make [task]\n\nTasks:"
	perl -nle 'printf("    \033[33m%-30s\033[0m %s\n",$$1,$$2) if /^([a-zA-Z_-]*?):(?:.+?## )?(.*?)$$/' $(MAKEFILE_LIST)

.SILENT: help

.PHONY: $(shell egrep -o '^(\._)?[a-z_-]+:' $(MAKEFILE_LIST) | sed 's/://')
