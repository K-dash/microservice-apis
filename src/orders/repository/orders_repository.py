from src.orders.orders_service.orders import Order
from src.orders.repository.models import OrderModel, OrderItemModel


class OrdersRepository:
    def __init__(self, session):
        self.session = session

    def add(self, items):
        # 注文のレコードを作成する際、注文内のアイテムごとにレコードを作成
        record = OrderModel(items=[OrderItemModel(**item) for item in items])
        # セッションオブジェクトにレコードを追加
        self.session.add(record)
        # Orderクラスのインスタンスを返す
        return Order(**record.dict(), order_=record)

    # IDでOrderModelのレコードを取得するための汎用メソッド
    def _get(self, id_):
        # SQLAlchemyのfirstメソッドを使ってレコードを取得
        return (
            self.session.query(OrderModel)
            .filter(OrderModel.id == str(id_))
            .first()
        )

    def get(self, id_):
        # _get()を使ってレコードを取得
        order = self._get(id_)
        # 注文が存在する場合はOrderオブジェクトを返す
        if order is not None:
            return Order(**order.dict())

    # limitパラメータとその他のオプションフィルタを受け取る
    def list(self, limit=None, **filters):
        # クエリを動的に構築
        query = self.session.query(OrderModel)
        # SQLAlchemyのfilterメソッドを使って注文がキャンセルされているかどうかを絞り込む
        if "cancelled" in filters:
            cancelled = filters.pop("cancelled")
            if cancelled:
                query = query.filter(OrderModel.status == "cancelled")
            else:
                query = query.filter(OrderModel.status != "cancelled")
        record = query.filter_by(**filters).limit(limit).all()
        # Orderオブジェクトのリストを返す
        return [Order(**order.dict()) for order in record]

    def update(self, id_, **payload):
        record = self._get(id_)
        # 注文を更新するためには、その注文に紐づけられたアイテムを削除した後、渡されたペイロードに基づいて新しいアイテムを作成する
        if "items" in payload:
            for item in record.items:
                self.session.delete(item)
            record.items = [
                OrderItemModel(**item) for item in payload.pop("items")
            ]

        # setattr関数を使ってデータベースオブジェクトを動的に更新
        for key, value in payload.items():
            setattr(record, key, value)
        return Order(**record.dict())

    def delete(self, id_):
        self.session.delete(self._get(id_))
