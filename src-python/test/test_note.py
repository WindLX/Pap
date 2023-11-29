from os import path

from .database_test_base import context

from pytest import mark
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder


@mark.usefixtures("context")
class TestNoteClass:

    def test_get_note(self, context: TestClient):
        response = context.get(
            "/note/get_notes")
        note_data = [
            {
                "id": 1,
                "name": "test",
                "tags": []
            }
        ]
        assert response.status_code == 200
        data = response.json()
        data[0].pop("url")
        assert data == jsonable_encoder(note_data)

    def test_delete_note(self, context: TestClient):
        delete_data = f"note_id={1}"
        response = context.delete(
            f"/note/delete_note?{delete_data}"
        )
        assert response.status_code == 200
