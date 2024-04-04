import yaml
from fastapi import FastAPI
from pathlib import Path

app = FastAPI(
    debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders"
)

# PyYAMLを使ってAPI仕様書を読み込む
oas_doc = yaml.safe_load(
    (Path(__file__).parent / "../oas.yaml").read_text()
)

app.openapi = lambda: oas_doc
from src.orders.api import api
