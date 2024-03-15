from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from homework_app.main import app
import json
import pytest

from homework_app.modules import KeyValue

client = TestClient(app)


def test_hello_endpoint():
    response = client.get("/hello")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.text == "HSE One Love!"


@pytest.mark.parametrize(("data", "status_code", "content_type"), [
    ({"key": "my_key", "value": "my_value"}, 200, "application/json"),
    ({"key": "my_key", "value": "my_value", "detail": "some info"}, 200, "application/json"),
    ("string", 415, "text/plain"),
    ({"value": "test_value"}, 400, "application/json"),
    ({}, 400, "application/json"),
    ({"key": "my_key", "value": True}, 400, "application/json"),
    ({"key": None, "value": "my_value"}, 400, "application/json"),
])
def test_set_endpoint(data, status_code, content_type):
    response = client.post("/set", json=data, headers={"content-type": content_type})
    assert response.status_code == status_code


@pytest.mark.parametrize(("data", "key", "status_code"), [
    ({"key": "my_key", "value": "my_value"}, "my_key", 200),
    ({"key": "my_key", "value": "my_value"}, "empty_key", 404)
])
def test_get_endpoint(data, key, status_code):
    client.post("/set", json=data)
    response = client.get(f"/get/{key}")
    assert response.status_code == status_code

    if response.status_code == status.HTTP_200_OK:
        assert response.headers.get('content-type') == "application/json"

        response_json = dict(json.loads(response.text))
        data = KeyValue(**response_json)
        if not data.key and not data.value:
            assert False


@pytest.mark.parametrize(("data", "status_code", "content_type"), [
    ({"dividend": 10, "divider": 2.5}, 200, "application/json"),
    ({"dividend": 10, "divider": 2.5, "detail": "some info"}, 200, "application/json"),
    ("string", 415, "text/plain"),
    ({"dividend": 10}, 400, "application/json"),
    ({"dividend": 10, "divider": 0}, 400, "application/json"),
    ({"dividend": True, "divider": "2.5"}, 400, "application/json"),
])
def test_divide_endpoint(data, status_code, content_type):
    response = client.post("/divide", json=data, headers={"content-type": content_type})
    assert response.status_code == status_code
    if response.status_code == status.HTTP_200_OK:
        assert response.headers.get('content-type') == 'text/plain; charset=utf-8'
        assert response.content.decode() == str(data["dividend"] / data["divider"])


@pytest.mark.parametrize(("path", "type"), [
    ("/hello/name", "GET"),
    ("/set/name", "POST"),
    ("/hello", "PUT"),
    ("/get/error", "PATCH"),
    ("/strange/path", "OPTIONS"),
    ("/name", "HEAD"),
])
def test_not_allowed_path(path: str, type: str):
    match type:
        case "GET": 
            assert client.get(path).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        case "PUT":
            assert client.put(path).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        case "DELETE":
            assert client.delete(path).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        case "POST":
            assert client.post(path).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        case "PATCH":
            assert client.patch(path).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        case "OPTIONS":
            assert client.options(path).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        case "HEAD":
            assert client.head(path).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
