from config import BaseConfig
from flask import Flask
from flask_smorest import Api
from src.kitchen.api.api import blueprint

app = Flask(__name__)

# Flaskのfrom_objectメソッドを使ってConfigクラスから設定を読み込む
app.config.from_object(BaseConfig)

kitchen_api = Api(app)

# Blueprintを厨房APIオブジェクトに登録
kitchen_api.register_blueprint(blueprint)
