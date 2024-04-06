from pathlib import Path
import yaml
from apispec import APISpec

from config import BaseConfig
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from src.kitchen.api.api import blueprint

app = Flask(__name__)
CORS(app)

# Flaskのfrom_objectメソッドを使ってConfigクラスから設定を読み込む
app.config.from_object(BaseConfig)

kitchen_api = Api(app)
# Blueprintを厨房APIオブジェクトに登録
kitchen_api.register_blueprint(blueprint)

api_spec = yaml.safe_load((Path(__file__).parent / "./oas.yaml").read_text())
spec = APISpec(
    title=api_spec["info"]["title"],
    version=api_spec["info"]["version"],
    openapi_version=api_spec["openapi"],
)
spec.to_dict = lambda: api_spec
kitchen_api.spec = spec
