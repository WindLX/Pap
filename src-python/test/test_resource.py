from .database_test_base import context
from schemas.resource import ResourceItemSchemaRelationship

from pytest import mark
from fastapi.encoders import jsonable_encoder


@mark.usefixtures("context")
class TestResourceClass:

    def test_create_resource_item(self, context):
        post_data = {
            "name": "test",
            "url": "/path/to/test"
        }
        response = context.post(
            "/resource/create_resource_item", json=post_data)
        assert response.status_code == 201
        resource_item_data = jsonable_encoder({
            "name": "test",
            "url": "/path/to/test"
        })
        assert response.json()["name"] == resource_item_data["name"]
        assert response.json()["url"] == resource_item_data["url"]
