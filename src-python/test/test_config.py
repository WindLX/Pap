from backend import app
from service.config import basic_config, path_config

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

client = TestClient(app)


def test_read_basic_config():
    response = client.get("/config/get_config/basic")
    assert response.status_code == 200
    basic_config_data = jsonable_encoder(basic_config.model)
    assert response.json() == basic_config_data


def test_write_basic_config():
    put_data = {
        "title": "Papp",
        "log_level": "DEBUG"
    }
    response = client.put("/config/set_config/basic", json=put_data)
    assert response.status_code == 202
    basic_config_data = jsonable_encoder(basic_config.model)
    assert put_data == basic_config_data
    put_data_2 = {
        "title": "Pap",
        "log_level": "DEBUG"
    }
    response_2 = client.put("/config/set_config/basic", json=put_data_2)
    assert response_2.status_code == 202


def test_read_path_config():
    response = client.get("/config/get_config/path")
    assert response.status_code == 200
    print(path_config.model)
    path_config_data = jsonable_encoder(path_config.model)
    assert response.json() == path_config_data


def test_read_config_error():
    response = client.get("/config/get_config/???")
    assert response.status_code == 404


def test_write_config_error():
    response = client.put("/config/set_config/???", json={})
    assert response.status_code == 404
