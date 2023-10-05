from os import path

from schemas.resource_base import ResourceItemSchemaCreate
from schemas.resource import ResourceItemSchemaRelationship
from service.config import path_config
from service.logger import logger
from service.database import get_db
from service.crud.resource import create_resource_item, get_resource_items

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends, UploadFile

router = APIRouter(prefix="/resource")


@router.post("/create_resource_item", status_code=status.HTTP_201_CREATED)
def create_resource(file: UploadFile, db: Session = Depends(get_db)):
    logger.info("POST /resource/create_resource_item")
    file_name = file.filename
    file_data = file.file.read()
    file_path = path.join(path_config.resource_dir, file_name)
    with open(file_path, 'wb') as fout:
        fout.write(file_data)
        file.file.close()
    resource_item = ResourceItemSchemaCreate(name=file_name, url=file_path)
    create_resource_item(db, resource_item=resource_item)


@router.get("/get_resource", response_model=list[ResourceItemSchemaRelationship])
def get_resource(db: Session = Depends(get_db)):
    logger.debug("GET /resource/get_resource")
    return get_resource_items(db)
