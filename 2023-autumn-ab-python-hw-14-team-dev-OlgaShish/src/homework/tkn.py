from typing import Any
from datetime import datetime, timedelta
import json
import jwt


class BadToken(Exception):
    "BadToken: compromised token"


def read_token(token: str) -> dict[str, Any]:
    """read token from dict by config key_word"""
    try:
        with open("config.json", encoding="utf-8") as config:
            key_word = json.load(config)["key_word"]
        jwt_token = jwt.decode(token, key_word, algorithms=["HS256"])
        return jwt_token
    except jwt.InvalidSignatureError:
        raise BadToken


def make_token(user_id: Any) -> str:
    """make token by config key_word and user_id"""
    with open("config.json", encoding="utf-8") as config:
        key_word = json.load(config)["key_word"]
    json_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = {"user_id": str(user_id), "time_created": str(json_time)}
    token = jwt.encode(body, key_word, algorithm="HS256")
    return token


def is_token_need_refresh(token: str) -> bool:
    """check if token isn't fresh and need refresh"""
    jwt_token = read_token(token)
    user_id = jwt_token.get("user_id", None)
    time_created = jwt_token.get("time_created", None)
    if user_id is None or time_created is None:
        raise BadToken
    time = datetime.strptime(jwt_token["time_created"], "%Y-%m-%d %H:%M:%S")
    with open("config.json", encoding="utf-8") as config:
        token_life = json.load(config)["token_life"]
    return datetime.now() - time > timedelta(hours=token_life)
