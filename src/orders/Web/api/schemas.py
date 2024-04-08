from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Extra, conint, conlist, validator


# 列挙スキーマを定義
class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"


class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    deliverd = "deliverd"


# pydanticモデルはそれぞれpydandicのBaseModelを継承する
class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1

    @validator("quantity")
    def quantity_non_nullable(cls, value):
        assert value is not None, "quantity may not be None"
        return value

    # Configを使ってスキーマで定義されたいないプロパティを禁止する
    class Config:
        extra = Extra.forbid


class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_length=1)

    class Config:
        extra = Extra.forbid


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]
