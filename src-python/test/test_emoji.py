from backend import app

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

client = TestClient(app)


def test_search_emoji():
    response = client.get("/emoji/get_emoji?emoji=smile")
    assert response.status_code == 200
    target_data = jsonable_encoder(
        [{"name": "cat with wry smile", "unicode": "U+1F63C"}])
    assert response.json() == target_data
