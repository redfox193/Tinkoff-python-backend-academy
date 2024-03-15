import pytest
from src.homework import tkn as token, main, tps as types, db_mock_methods
from fastapi import HTTPException
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from freezegun import freeze_time
import asyncio

client = TestClient(main.app)


def test_read_token_is_none():
    jwt_token = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjN9.\
V8ELQLA8XEwR4JDqFIM45MUzuQ75NyIjqheefo6Gmag"
    with pytest.raises(token.BadToken):
        token.read_token(jwt_token)


def test_is_token_need_refresh():
    jwt_token = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
eyJ1c2VyX2lkIjoxMjMsInRpbWVfY3JlYXRlZCI6IjIwMjMtMTItMjUgMDU6NTc6MzIifQ.\
FXoSunMxvgjY8BIl6bwq24obWoFuiwMzwH91jQFcVgk"
    op = token.is_token_need_refresh(jwt_token)
    assert op

    jwt_token = token.make_token("123")
    op = token.is_token_need_refresh(jwt_token)
    assert not op


def test_get_token():
    jwt_token = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
eyJ1c2VyX2lkIjoxMjMsInRpbWVfY3JlYXRlZCI6IjIwMjMtMTItMjUgMDU6NTc6MzIifQ.\
FXoSunMxvgjY8BIl6bwq24obWoFuiwMzwH91jQFcVgk"
    with pytest.raises(HTTPException):
        asyncio.run(main.get_token(jwt_token))


def test_registaration_and_authorization(mocker):
    body = {
        "login": "login",
        "password": "password",
        "first_name": "first_name",
        "second_name": "second_name",
        "skils": ["skil1", "skil2"],
        "company": "company",
    }
    mocker.patch.object(db_mock_methods, "add_user", return_value="123")

    response = client.post("/registration", json=body)
    assert response.status_code == 200
    jwt_token = response.json()
    assert not token.is_token_need_refresh(jwt_token)

    body = {"login": "login", "password": "password", "token": jwt_token}

    user_info = types.User("login", "password", "", "", False, [], None, {})

    mocker.patch.object(db_mock_methods, "find_user", return_value=user_info)
    response = client.post("/authorization", json=body)

    assert response.status_code == 200
    assert response.json() == jwt_token

    cur_time = datetime.now() + timedelta(hours=2)
    with freeze_time(cur_time):
        response = client.post("/authorization", json=body)
        assert response.status_code == 200
        assert response.json() != jwt_token

    user_info = {"login": "login", "password": "pas", "token": jwt_token}

    response = client.post("/authorization", json=user_info)

    assert response.status_code == 400
    assert response.text == '{"detail":"Bad password"}'

    user_info["login"] = "log"
    response = client.post("/authorization", json=user_info)

    assert response.status_code == 400
    assert response.text == '{"detail":"Bad login"}'


def test_create_post():
    jwt_token = token.make_token("123")

    body = {
        "post_id": None,
        "name": "name",
        "text": "text",
        "tags": [],
        "token": jwt_token,
        "new_likes": None,
        "new_dislikes": None,
        "new_comments": [],
    }
    res = client.post("/create_post", json=body)
    assert res.status_code == 200


def test_delete_post(mocker):
    jwt_token = token.make_token("123")

    body = {"post_id": "123", "token": jwt_token}

    post_info = types.Post(
        name="name",
        text="text",
        author_id="123",
        tags=[],
        comments=[],
        likes=0,
        dislikes=0,
    )

    mocker.patch.object(db_mock_methods, "find_post", return_value=post_info)
    res = client.post("/delete_post", json=body)

    assert res.status_code == 200

    post_info.author_id = "124"

    mocker.patch.object(db_mock_methods, "find_post", return_value=post_info)
    res = client.post("/delete_post", json=body)

    assert res.status_code == 400

    post_info = None

    mocker.patch.object(db_mock_methods, "find_post", return_value=post_info)
    res = client.post("/delete_post", json=body)

    assert res.status_code == 400


def test_update_post(mocker):
    jwt_token = token.make_token("123")

    body = {
        "post_id": None,
        "name": "name",
        "text": "text",
        "tags": [5],
        "token": jwt_token,
        "new_likes": 3,
        "new_dislikes": None,
        "new_comments": ["comment"],
    }

    res = client.post("/update_post", json=body)

    assert res.status_code == 400

    body["post_id"] = "123"

    db_post = types.Post(
        name="name",
        text="text",
        author_id="123",
        tags=[],
        comments=[],
        likes=0,
        dislikes=0,
    )
    mocker.patch.object(db_mock_methods, "find_post", return_value=db_post)
    db_user = types.User(
        login="login",
        password="password",
        first_name="first_name",
        second_name="second_name",
        is_admin=False,
        skils=[],
        company=None,
        posts_ids_to_names={},
    )
    mocker.patch.object(db_mock_methods, "find_user", return_value=db_user)

    res = client.post("/update_post", json=body)

    assert res.status_code == 200


def test_get_posts():
    body = {
        "author_id": "123",
        "tags": [1],
        "name_search": "help",
        "pagination_current": 0,
    }

    res = client.post("/get_posts", json=body)

    assert res.status_code == 200
