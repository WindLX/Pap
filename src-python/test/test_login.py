from backend import app

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

client = TestClient(app)


def test_login():
    post_data = {
        "password": ""
    }
    response = client.post("/login", json=post_data)
    assert response.status_code == 200
    print(response.json())
