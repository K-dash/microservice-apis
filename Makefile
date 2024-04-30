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
	export FLASK_APP=src/kitchen/app.py && rye run flask run --host=0.0.0.0 --port=3000 --reload

# run products for uvicorn
.PHONY: run_uvicorn_for_products
run_uvicorn_for_products:
	rye run uvicorn src.products.server:server --reload

# generate jwt
.PHONY: generate_jwt
generate_jwt:
	rye run python src/jwt_generator.py

# run order api test with dredd.PHONY: all start_mocks run_dredd stop_mocks
.PHONY: all start_mocks run_dredd stop_mocks
run_orders_api_test_with_dredd: start_mocks run_dredd stop_mocks

start_mocks:
	cd src/orders && yarn prism mock kitchen.yaml --port 3000 &
	cd src/orders && yarn prism mock payments.yaml --port 3001 &
	sleep 5

run_dredd:
	export PATH=".venv/bin:$$PATH" && dredd src/orders/oas.yaml http://127.0.0.1:8000 --server "rye run uvicorn src.orders.Web.app:app" --hookfiles=src/orders/hooks.py --language=python

stop_mocks:
	kill $$(lsof -ti:3000) $$(lsof -ti:3001)

# run order api test witch schemathesis
.PHONY: run_orders_api_test_with_schemathesis
run_orders_api_test_with_schemathesis: start_orders_api run_schemathesis

start_orders_api:
	rye run uvicorn src.orders.Web.app:app --reload &

run_schemathesis:
	rye run schemathesis run src/orders/oas.yaml --base-url=http://127.0.0.1:8000 --hypothesis-database=none --stateful=links --checks=all --hypothesis-suppress-health-check=too_slow
