from typing import Optional

from schemas.resource_base import ResourceItemSchemaCreate
from schemas.resource import ResourceItemSchemaRelationship
from service.logger import logger
from service.database import get_db
from service.crud.resource import create_resource_item

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends

router = APIRouter(prefix="/resource")


@router.post("/create_resource_item", response_model=ResourceItemSchemaRelationship, status_code=status.HTTP_201_CREATED)
def create_resource(resource_item: ResourceItemSchemaCreate, db: Session = Depends(get_db)):
    logger.info("POST /resource/create_resource_item")
    return create_resource_item(db, resource_item=resource_item)
