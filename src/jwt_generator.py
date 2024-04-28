from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import jwt
from cryptography.hazmat.primitives import serialization


def generate_jwt():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    payload = {
        "iss": "https://auth.hogefuga.piyo/",
        "sub": "ec7bbccf-ca89-3af5-22ba-c53a4553b134",
        "aud": "http://127.0.0.1:8000/orders/",
        "iat": now.timestamp(),
        "exp": (now + timedelta(hours=1)).timestamp(),
        "scope": "openid",
    }
    private_key_text = Path("cert/private_key.pem").read_text()
    private_key = serialization.load_pem_private_key(
        private_key_text.encode(), password=None
    )
    return jwt.encode(payload, private_key, algorithm="RS256")


print(generate_jwt())
