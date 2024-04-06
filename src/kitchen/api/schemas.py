from enum import Enum

from marshmallow import EXCLUDE, Schema, fields, validate


class OrderStatus(Enum):
    PENDING = "pending"
    PROGRESS = "progress"
    CANCELLED = "cancelled"
    FINISHED = "finished"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class OrderItemSchema(Schema):
    # Metaクラスで未知のプロパティを禁止する
    class Meta:
        unknown = EXCLUDE

    product = fields.String(required=True)
    size = fields.String(
        validate=validate.OneOf(["small", "medium", "big"]), required=True
    )
    quantity = fields.Integer(
        validate=validate.Range(1, min_inclusive=True), required=True
    )


class ScheduleOrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    order = fields.List(fields.Nested(OrderItemSchema), required=True)


# クラス継承を使って既存のスキーマの定義(orderプロパティ)を再利用する
class GetScheduledOrderSchema(ScheduleOrderSchema):
    id = fields.UUID(required=True)
    scheduled = fields.DateTime(required=True)
    status = fields.String(
        required=True,
        validate=validate.OneOf(OrderStatus.list()),
    )


class GetScheduledOrdersSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    schedules = fields.List(fields.Nested(GetScheduledOrderSchema), required=True)


class ScheduleStatusSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status = fields.String(
        required=True,
        validate=validate.OneOf(OrderStatus.list()),
    )


# /kitchen/schedules/のURLパラメータを定義
class GetKitchenScheduleParametars(Schema):
    class Meta:
        unknown = EXCLUDE

    progress = fields.Boolean(required=False)
    limit = fields.Integer(required=False)
    since = fields.DateTime(required=False)
