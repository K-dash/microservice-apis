from src.orders.orders_service.exceptions import OrderNotFoundError


class OrdersService:
    def __init__(self, orders_repository):
        # OrderServiceの中でOrderRepositoryをインスタンス化するのはアンチパターン
        # OrderServiceがOrderRepositoryに依存するだけでなく、OrderServiceがOrderRepositoryの実装の詳細（インスタンス化の方法等）を知る必要がある
        # self.orders_repository = OrdersRepository()

        # DIでOrderRepositoryインスタンスを注入する
        # これにより、OrderServiceはOrderRepositoryの実装の詳細を知る必要がなくなる
        # こうすることで、OrderRepositoryのインスタンス化と設定を行う責務はOrderServiceを呼び出す側に委ねられる
        self.orders_repository = orders_repository

    def place_order(self, items, user_id):
        return self.orders_repository.add(items, user_id)

    def get_order(self, order_id, **filters):
        order = self.orders_repository.get(order_id, **filters)
        if order is not None:
            return order
        raise OrderNotFoundError(f"Order with id {order_id} not found")

    def update_order(self, order_id, user_id, **payload):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        return self.orders_repository.update(order_id, **payload)

    def list_orders(self, **filters):
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit=limit, **filters)

    def pay_order(self, order_id, user_id):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        order.pay()
        schedule_id = order.schedule()
        return self.orders_repository.update(
            order_id, status="progress", schedule_id=schedule_id
        )

    def cancel_order(self, order_id, user_id):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        order.cancel()
        return self.orders_repository.update(order_id, status="cancelled")

    def delete_order(self, order_id, user_id):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        return self.orders_repository.delete(order_id)
