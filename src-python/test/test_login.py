from backend import app

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

client = TestClient(app)


def test_login():
    post_data = {
        "username": "test",
        "password": "1234"
    }
    response = client.post("/login", data=post_data)
    assert response.status_code == 200
    print(response.json())
