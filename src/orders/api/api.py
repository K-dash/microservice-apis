from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from src.orders.app import app
from starlette import status
from starlette.responses import Response

orders = {
    "id": "ff0f1355-e821-4178-9567-550dec27a373",
    "status": "deliverd",
    "created": datetime.now(ZoneInfo("Asia/Tokyo")),
    "order": [
        {
            "product": "Coffee",
            "size": "small",
            "quantity": 1,
        },
    ],
}


@app.get("/orders")
async def get_orders() -> dict:
    return orders


@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order() -> dict:
    return orders


@app.get("/orders/{order_id}")
def get_order(order_id: UUID) -> dict:
    return orders


@app.put("/orders/{order_id}")
def update_order(order_id: UUID) -> dict:
    return orders


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: UUID) -> dict:
    return orders


@app.post("/orders/{order_id}/pay")
async def pay_order(order_id: UUID) -> dict:
    return orders
