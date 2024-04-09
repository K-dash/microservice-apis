import requests

from src.orders.orders_service.exceptions import (
    APIIntegrationError, InvalidActionError
)

# 注文アイテムを表すビジネスオブジェクト（ドメインオブジェクト）
class OrderItem:
    def __init__(self, id, product, quantity, size):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.size = size

    def dict(self):
        return {
            'product': self.product,
            'size': self.size,
            'quantity': self.quantity
        }


class Order:
    def __init__(self, id, created, items, status, schedule_id=None, delivery_id=None, order_=None):
        # order_パラメータはデータベースモデルのインスタンスを表す
        self._order = order_
        # IDは動的に解決するため、指定あれたIDをプライベートプロパティとして保存
        self._id = id
        self._created = created
        self._status = status
        # 注文アイテムごとにOrderItemオブジェクトを構築
        self.items = [OrderItem(**item) for item in items]
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id

    @property
    def id(self):
        return self._id or self._order.id

    @property
    def created(self):
        return self._created or self._order.created

    @property
    def status(self):
        return self._status or self._order.status

    def cancel(self):
        # 注文が処理中の場合は、厨房APIに注文のキャンセルリクエストを送信
        if self.status == "progress":
            kitchen_base_url = "http://127.0.0.1:3000/kitchen"
            response = requests.post(
                f"{kitchen_base_url}/schedule/{self.schedule_id}/cancel",
                json={"order": [item.dict() for item in self.items]},
            )
            # 厨房APIから成功のレスポンスを受け取った場合は呼び出し元に戻る
            if response.status_code == 200:
                return
            raise APIIntegrationError(
                f"Could not cancel order with id {self.id}"
            )
        # 配達中の注文のキャンセルは許可しない
        if self.status == "delivery":
            raise InvalidActionError(
                f"Could not cancel order with id {self.id}"
            )

    def pay(self):
        # 支払いAPIを呼び出して支払いを行う
        response = requests.post(
            "http://127.0.0.1:3001/payments", json={"order_id": self.id, "status": "paid"}
        )
        if response.status_code == 201:
            return
        raise APIIntegrationError(
            f"Could not process payment for order with id {self.id}"
        )

    def schedule(self):
        # 厨房APIを呼び出して注文の製造をスケジュール
        response = requests.post(
            "http://localhost:3000/kitchen/schedules",
            json={"order": [item.dict() for item in self.items]},
        )
        # 厨房APIから成功のレスポンスを受け取った場合は呼び出し元に戻る
        if response.status_code == 201:
            return
        raise APIIntegrationError(
            f"Could not schedule order with id {self.id}"
        )

    def dict(self):
        return {
            'id': self.id,
            'order': [item.dict() for item in self.items],
            'status': self.status,
            'created': self.created,
        }

