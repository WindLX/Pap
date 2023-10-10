from backend import app
from model.resource_group import Base
from schemas.resource_base import ResourceItemSchemaCreate
from service.database import get_db
from service.crud.resource import create_resource_item

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


@fixture
def context():
    SQLALCHEMY_DATABASE_URL = "./data/fake_tag.db"
    db = open(SQLALCHEMY_DATABASE_URL, 'w')
    db.close()

    engine = create_engine(f'sqlite:///{SQLALCHEMY_DATABASE_URL}',
                           connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with SessionLocal() as db:
        create_resource_item(db, ResourceItemSchemaCreate(
            name="test", url="/path/to/test"))

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
