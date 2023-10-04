from backend import app
from service.config import system_config, path_config

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

client = TestClient(app)


def test_read_system_config():
    response = client.get("/api/get_config/system")
    assert response.status_code == 200
    system_config_data = jsonable_encoder(system_config.model)
    assert response.json() == system_config_data


def test_write_system_config():
    put_data = {
        "host": "127.0.0.1",
        "port": 8001,
        "title": "Pap",
        "log_level": "DEBUG"
    }
    response = client.put("/api/set_config/system", json=put_data)
    assert response.status_code == 202
    system_config_data = jsonable_encoder(system_config.model)
    assert put_data == system_config_data
    put_data_2 = {
        "host": "127.0.0.1",
        "port": 8000,
        "title": "Pap",
        "log_level": "DEBUG"
    }
    response_2 = client.put("/api/set_config/system", json=put_data_2)
    assert response_2.status_code == 202


def test_read_path_config():
    response = client.get("/api/get_config/path")
    assert response.status_code == 200
    path_config_data = jsonable_encoder(path_config.model)
    assert response.json() == path_config_data


def test_write_path_config():
    put_data = {
        "resource_dir": "./data/resource/",
        "content_dir": "./data/content/",
        "log_path": "./data/pap.log",
        "tag_path": "./data/tags.toml"
    }
    response = client.put("/api/set_config/path", json=put_data)
    assert response.status_code == 202
    path_config_data = jsonable_encoder(path_config.model)
    assert put_data == path_config_data
    put_data_2 = {
        "resource_dir": "./data/resource/",
        "content_dir": "./data/content/",
        "log_path": "./data/pap.log",
        "tag_path": "./data/tag.toml"
    }
    response_2 = client.put("/api/set_config/path", json=put_data_2)
    assert response_2.status_code == 202


def test_read_config_error():
    response = client.get("/api/get_config/???")
    assert response.status_code == 404


def test_write_config_error():
    response = client.put("/api/set_config/???", json={})
    assert response.status_code == 404
