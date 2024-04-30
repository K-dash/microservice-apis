from pathlib import Path

import hypothesis.strategies as st
import jsonschema
import yaml
from fastapi.testclient import TestClient
from hypothesis import given, Verbosity, settings
from jsonschema import ValidationError, RefResolver

from src.orders.Web.app import app

# API仕様を読み込む
orders_api_spec = yaml.full_load(
    (Path(__file__).parent / "oas.yaml").read_text()
)

# # API仕様の中のCreateOrderSchemaのポインタを取得
create_order_schema = orders_api_spec["components"]["schemas"]["CreateOrderSchema"]

# ペイロードがAPI仕様に準拠しているかどうかを判断するためのヘルパー関数
def is_valid_payload(payload, schema):
    try:
        jsonschema.validate(
            payload, schema=schema,
            resolver=RefResolver("", orders_api_spec)
        )
    except ValidationError:
        return False
    else:
        return True


test_client = TestClient(app=app)

# リクエストペイロードがとり得るすべての値を定義
values_strategy = (
        st.none() |
        st.booleans() |
        st.text() |
        st.integers()
)

# テスト用のペイロードを作成
order_item_strategy = st.fixed_dictionaries(
    {
        "product": values_strategy,
        "size": st.one_of(st.sampled_from(("small", "medium", "big"))) | values_strategy,
        "quantity": values_strategy
    }
)
strategy = st.fixed_dictionaries({
    "order": st.lists(order_item_strategy)
})


# given() を使ってHypothesisのストラテジをテスト関数に与え、payload引数を使って各テストケースを取得
@settings(verbosity=Verbosity.verbose, max_examples=500)
@given(strategy)
def test(payload):
    # テスト実行
    response = test_client.post("/orders", json=payload)
    # ペイロードがAPI仕様に準拠しているかどうかを判断
    if is_valid_payload(payload, create_order_schema):
        assert response.status_code == 201
    else:
        assert response.status_code == 422
