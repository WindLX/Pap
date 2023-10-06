from .database_test_base import context

from pytest import mark
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder


@mark.usefixtures("context")
class TestResourceClass:

    def test_get_resource(self, context: TestClient):
        response = context.get(
            "/resource/get_resource")
        resource_data = [
            {
                "id": 1,
                "name": "test",
                "url": "/path/to/test",
                "contents": [],
                "tags": []
            }
        ]
        assert response.status_code == 200
        assert response.json() == jsonable_encoder(resource_data)

    def test_delete_resource_item(self, context: TestClient):
        post_data = {
            "name": "test_content",
            "resource_item_id": 1
        }
        response = context.post(
            "/resource/create_content", json=post_data)
        assert response.status_code == 201
        delete_data = f"resource_item_id={1}"
        response_2 = context.delete(
            f"/resource/delete_resource_item?{delete_data}"
        )
        assert response_2.status_code == 200
        response_3 = context.get(
            f"/resource/get_resource"
        )
        content = response_3.json()
        assert content == []
