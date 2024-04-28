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
.PHONY: run_uvicorn_for_orders
run_uvicorn_for_orders:
	rye run uvicorn src.orders.Web.app:app --reload

# run kitchen for flask
.PHONY: run_flask
run_flask:
	export FLASK_APP=src/kitchen/app.py && rye run flask run --host=0.0.0.0 --port=4000 --reload

# run products for uvicorn
.PHONY: run_uvicorn_for_products
run_uvicorn_for_products:
	rye run uvicorn src.products.server:server --reload

# generate jwt
.PHONY: generate_jwt
generate_jwt:
	rye run python src/jwt_generator.py
