

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fmt: ## Run black to format code
	pipenv run black .

test:  ## Run pytest for files under ./tests
	python -m pytest --nf --ff ./integration_tests

test-all:  ## Run pytest for all files
	@export $(sed 's/#.*//g' .env | xargs) >/dev/null 2>&1
	run python -m pytest --nf --ff .

# setup:  ## Run pipenv install to setup the environment
# 	pip install --dev --skip-lock
# 	pip run pre-commit install
# 	pip run pre-commit install-hooks
