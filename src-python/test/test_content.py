from os import path

from .database_test_base import context

from pytest import mark
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder


@mark.usefixtures("context")
class TestContentClass:

    def test_create_content(self, context: TestClient):
        post_data = {
            "name": "test_content",
            "resource_item_id": 1
        }
        response = context.post(
            "/resource/create_content", json=post_data)
        assert response.status_code == 201
        resource_item_data = jsonable_encoder({
            "name": "test",
            "url": "/path/to/test",
            "contents": [post_data]
        })
        assert response.json()["name"] == resource_item_data["name"]
        assert response.json()["url"] == resource_item_data["url"]
        assert response.json()[
            "contents"][0]["name"] == resource_item_data["contents"][0]["name"]

    def test_delete_content(self, context: TestClient):
        post_data = {
            "name": "test_content",
            "resource_item_id": 1
        }
        response = context.post(
            "/resource/create_content", json=post_data)
        assert response.status_code == 201
        delete_data = f"content_id={1}"
        response_2 = context.delete(
            f"/resource/delete_content?{delete_data}"
        )
        assert response_2.status_code == 200
        response_3 = context.get(
            f"/resource/get_resource"
        )
        content = response_3.json()[0]["contents"]
        assert content == []
        assert path.exists(response.json()["contents"][0]["url"]) == False
