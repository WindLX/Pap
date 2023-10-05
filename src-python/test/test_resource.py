from os import remove

from backend import app
from model.resource_group import Base
from service.database import get_db
from schemas.resource import ResourceItemSchemaRelationship

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

SQLALCHEMY_DATABASE_URL = "./data/fake_tag.db"
db = open(SQLALCHEMY_DATABASE_URL, 'w')
db.close()

engine = create_engine(f'sqlite:///{SQLALCHEMY_DATABASE_URL}',
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db


def test_create_resource_item():
    post_data = {
        "name": "test",
        "url": "/path/to/test"
    }
    response = client.post("/resource/create_resource_item", json=post_data)
    assert response.status_code == 201
    resource_item_data = jsonable_encoder({
        "name": "test",
        "url": "/path/to/test"
    })
    assert response.json()["name"] == resource_item_data["name"]
    assert response.json()["url"] == resource_item_data["url"]
    remove(SQLALCHEMY_DATABASE_URL)
