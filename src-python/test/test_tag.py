from os import path

from .database_test_base import context

from pytest import mark
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder


@mark.usefixtures("context")
class TestTagClass:

    def test_create_tag(self, context: TestClient):
        post_data = {
            "name": "test_tag",
            "color": "#FFFFFF",
            "note_id": 1
        }
        response = context.post(
            "/tag/create_tag", json=post_data)
        assert response.status_code == 201
        assert response.json()["name"] == post_data["name"]
        assert response.json()["color"] == post_data["color"]
        assert response.json()[
            "notes"][0]["id"] == 1

    def test_update_tag(self, context: TestClient):
        post_data = {
            "name": "test_tag",
            "color": "#FFFFFF",
            "note_id": 1
        }
        response = context.post(
            "/tag/create_tag", json=post_data)
        assert response.status_code == 201
        post_data = {
            "name": "test_new_tag",
            "color": "#FFAFAF",
            "id": 1
        }
        response = context.put(
            "/tag/update_tag", json=post_data)
        assert response.status_code == 202
        assert response.json()["name"] == post_data["name"]
        assert response.json()["color"] == post_data["color"]

    def test_remove_tag(self, context: TestClient):
        post_data = {
            "name": "test_tag",
            "color": "#FFFFFF",
            "note_id": 1
        }
        response = context.post(
            "/tag/create_tag", json=post_data)
        assert response.status_code == 201
        response = context.put(
            "/tag/remove_tag?tag_id=1&note_id=1")
        assert response.status_code == 202
        response = context.get("/tag/get_tags")
        assert response.status_code == 200
        assert response.json()[0]["id"] == 1
        response = context.get("/note/get_notes")
        assert response.status_code == 200
        assert len(response.json()[0]["tags"]) == 0

    def test_delete_tag(self, context: TestClient):
        post_data = {
            "name": "test_tag",
            "color": "#FFFFFF",
            "note_id": 1
        }
        response = context.post(
            "/tag/create_tag", json=post_data)
        assert response.status_code == 201
        response = context.delete("/tag/delete_tag?tag_id=1")
        assert response.status_code == 200
        response = context.get("/tag/get_tags")
        assert response.status_code == 200
        assert len(response.json()) == 0
        response = context.get("/note/get_notes")
        assert response.status_code == 200
        assert len(response.json()[0]["tags"]) == 0
