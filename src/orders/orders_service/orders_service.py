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

    def place_order(self, items):
        return self.orders_repository.add(items)

    def get_order(self, order_id):
        # 注文リポジトリにリクエストされたIDを渡して注文の詳細を取得
        order = self.orders_repository.get(order_id)
        # 注文が存在しない場合は、OrderNotFoundError例外を送出
        if order is not None:
            return order
        raise OrderNotFoundError(f"Order with id {order_id} not found")

    def update_order(self, order_id, **payload):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')
        return self.orders_repository.update(order_id, **payload)

    def list_orders(self, **filters):
        # キーワード引数を使ってフィルタをdictとしてキャプチャ
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit, **filters)

    def pay_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        order.pay()
        # 注文をスケジュールした後、schedule_id属性を更新
        schedule_id = order.schedule()
        return self.orders_repository.update(
            order_id, status="progress", schedule_id=schedule_id
        )

    def cancel_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        order.cancel()
        return self.orders_repository.update(order_id, status="cancelled")

    def delete_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')
        return self.orders_repository.delete(order_id)
