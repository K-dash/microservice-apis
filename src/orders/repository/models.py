import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()   # 宣言的なベースモデルを作成

def generate_uuid():
    return str(uuid.uuid4())


# すべてのモデルがBaseを継承する必要がある
class OrderModel(Base):
    __tablename__ = "order"

    # 各プロパティはColumnクラスを使ってデータベースの列にマッピングされる
    id = Column(String, primary_key=True, default=generate_uuid)
    status = Column(String, nullable=False, default="created")
    created = Column(DateTime, default=datetime.now(ZoneInfo("Asia/Tokyo")))
    schedule_id = Column(String)
    delivery_id = Column(String)
    # relationship()メソッドを使ってOrderItemModelと1対多の関係を定義
    # OrderModelから"order"というプロパティを通じてOrderItemModelにアクセスが可能になる
    items = relationship("OrderItemModel", backref="order")

    # オブジェクトをDict形式にレンダリングするためのカスタムメソッド
    def dict(self):
        return {
            "id": self.id,
            "items": [item.dict() for item in self.items],
            "status": self.status,
            "created": self.created,
            "schedule_id": self.schedule_id,
            "delivery_id": self.delivery_id,
        }


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    # 外部キーとして、orderテーブルのidを参照する
    order_id = Column(String, ForeignKey("order.id"))
    product = Column(String, nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    # オブジェクトをDict形式にレンダリングするためのカスタムメソッド
    def dict(self):
        return {
            "id": self.id,
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity,
        }
