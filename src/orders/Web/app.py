import os
import yaml
from fastapi import FastAPI
from pathlib import Path

from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidAlgorithmError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)

from starlette import status
from starlette.middleware.base import (
    RequestResponseEndpoint,
    BaseHTTPMiddleware
)
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.orders.Web.api.auth import decode_and_validate_token


app = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")

# PyYAMLを使ってAPI仕様書を読み込む
oas_doc = yaml.safe_load((Path(__file__).parent / "../oas.yaml").read_text())

app.openapi = lambda: oas_doc

# StarletteのBaseHTTPMiddlewareを継承して、認可用のミドルウェアクラスを定義
class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    # ミドルウェアのエントリポイント
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        # AUTH_ON の環境変数に応じて処理を分ける
        if os.getenv("AUTH_ON", "False") != "True":
            # Falseの場合は デフォルトユーザーを「test」にする
            request.state.user_id = "test"
            return await call_next(request)

        # OpenAPIドキュメントのエンドポイントは公開したいので認可を必要としない
        if request.url.path in ["/openapi/orders.json", "/docs/orders"]:
            return await call_next(request)
        # CORSリクエストも認可を必要としない
        if request.method == "OPTIONS":
            return await call_next(request)

        # Authorizationヘッダーを取得
        bearer_token = request.headers.get("Authorization")
        # Authorizationヘッダーが無い場合は401エラー
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "access token is missing",
                    "body": "access token is missing",
                }
            )

        try:
            # トークンを検証
            auth_token = bearer_token.split(" ")[1].strip()
            # トークンのペイロードを検証して取得
            token_payload = decode_and_validate_token(access_token=auth_token)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAudienceError,
            InvalidAlgorithmError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError
        ) as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": str(e),
                    "body": str(e),
                }
            )
        else:
            # トークンのsubフィールドからユーザーIDを取得
            request.state.user_id = token_payload["sub"]
        return await call_next(request)

# ミドルウェアを設定
app.add_middleware(AuthorizeRequestMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.orders.Web.api import api
