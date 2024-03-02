# install
.PHONY: install
install:
	rye pin 3.10
	rye sync
	rye run pre-commit install
	### create .env
	@if [ ! -f env/.env ]; then \
        cp env/.env.example env/.env; \
        echo "Created .env file from .env.example"; \
    fi

# main.py
.PHONY: run_main
run_main:
	python src/main.py

# pre-commit
.PHONY: pre-commit
pre-commit:
	rye run pre-commit run --all-files

# test
.PHONY: test
test:
	rye run pytest tests
