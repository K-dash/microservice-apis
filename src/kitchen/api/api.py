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
    GetKitchenScheduleParametars,
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
    # locatino=queryでURLパラメータを受け取る
    @blueprint.arguments(GetKitchenScheduleParametars, location="query")
    # Blueprintのresponse()デコレータを使ってレスポンスペイロードのmarshmallowモデル定義
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def get(self, parameters):
        if not parameters:
            return {"schedules": schedules}
        # queryパラメータをもとにクエリを絞り込む
        query_set = [schedule for schedule in schedules]

        # progress
        in_progress = parameters.get("in_progress")
        if in_progress is not None:
            query_set = [
                schedule
                for schedule in query_set
                if schedule["status"] == "progress" == in_progress
            ]

        # cancelled
        cancelled = parameters.get("cancelled")
        if cancelled is not None:
            query_set = [
                schedule
                for schedule in query_set
                if schedule["status"] == "cancelled" == cancelled
            ]

        # limit
        limit = parameters.get("limit")
        if limit is not None and len(query_set) > limit:
            query_set = query_set[:limit]

        return {"schedules": query_set}


    # Blueprintのargments()デコレーターを使ってリクエストペイロードのmarshmallowモデルを定義
    @blueprint.arguments(ScheduleOrderSchema) #scheduleOrderSchemaモデルの定義に従ってリクエストペイロードの検証とマーシャリングが行われる
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
