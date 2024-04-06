import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from flask.views import MethodView
from flask_smorest import Blueprint
from src.kitchen.api.schemas import (
    GetScheduledOrderSchema,
    GetScheduledOrdersSchema,
    ScheduleOrderSchema,
    ScheduleStatusSchema,
)

# flask-somorestのBlueprintクラスのインスタンスを作成
blueprint = Blueprint("kitchen", __name__, description="Kitchen API")

# 一旦、仮のレスポンスをハードコードする
schedules = [
    {
        "id": uuid.uuid4(),
        "schedule": datetime.now(ZoneInfo("Asia/Tokyo")),
        "status": "pending",
        "order": [{"product": "hamburger", "quantity": 1, "size": "small"}],
    }
]


# Blueprintのroute()デコレータを使ってクラスベースのルーティングを定義
@blueprint.route("/kitchen/schedules")
class KitchenSchedules(MethodView):
    # Blueprintのresponse()デコレータを使ってレスポンスペイロードのmarshmallowモデル定義
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def get(self):
        return {"schedules": schedules}

    # Blueprintのargments()デコレーターを使ってリクエストペイロードのmarshmallowモデル定義
    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduledOrderSchema)
    def post(self):
        return schedules[0]


@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSchedule(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self, schedule_id):
        return schedules[0]

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def put(self, payload, schedule_id):
        return schedules[0]

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        return


# 関数ベースのビューのルーティングを定義
@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
def cancel_schedule(schedule_id):
    return schedules[0]


@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
def get_schedule_status(schedule_id):
    return schedules[0]
