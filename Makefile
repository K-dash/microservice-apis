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

# run orders for uvicorn
.PHONY: run_uvicorn
run_uvicorn:
	rye run uvicorn src.orders.app:app --reload

# run kitchen for flask
.PHONY: run_flask
run_flask:
	export FLASK_APP=src/kitchen/app.py
	rye run flask run --reload
