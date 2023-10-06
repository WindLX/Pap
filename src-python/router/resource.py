from os import path

from schemas.resource_base import ResourceItemSchemaCreate
from schemas.resource import ResourceItemSchemaRelationship
from schemas.content import ContentSchemaCreate
from service.config import path_config
from service.logger import logger
from service.database import get_db
from service.crud import resource, content

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends, UploadFile

router = APIRouter(prefix="/resource")


@router.post("/create_resource_item", status_code=status.HTTP_201_CREATED)
def create_resource(file: UploadFile, db: Session = Depends(get_db)):
    """create a new resource item from upload file

    Args:
        file (UploadFile): upload file from frontend
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("POST /resource/create_resource_item")
    file_name = file.filename
    file_data = file.file.read()
    file_path = path.join(path_config.resource_dir, file_name)
    with open(file_path, 'wb') as fout:
        fout.write(file_data)
        file.file.close()
    resource_item = ResourceItemSchemaCreate(name=file_name, url=file_path)
    resource.create_resource_item(db, resource_item=resource_item)


@router.get("/get_resource", response_model=list[ResourceItemSchemaRelationship])
def get_resource(db: Session = Depends(get_db)) -> list[ResourceItemSchemaRelationship]:
    """get all resource items

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    logger.debug("GET /resource/get_resource")
    return resource.get_resource_items(db)


@router.delete("/delete_resource_item", status_code=status.HTTP_200_OK)
def delete_resource_item(resource_item_id: int, db: Session = Depends(get_db)):
    """delete resource item by resource item id

    Args:
        resource_item_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("DELETE /resource/delete_resource_item")
    resource.delete_resource_item(db, resource_item_id)


@router.post("/create_content", response_model=ResourceItemSchemaRelationship, status_code=status.HTTP_201_CREATED)
def create_content(new_content: ContentSchemaCreate, db: Session = Depends(get_db)) -> ResourceItemSchemaRelationship:
    """create a new content to a resource item

    Args:
        new_content (ContentSchemaCreate): new content data
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target resource item

    Returns:
        ResourceItemSchemaRelationship: updated resource item
    """
    logger.info("POST /resource/create_content")
    if updated_resource_item := content.create_content(db, new_content):
        return updated_resource_item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/delete_content", status_code=status.HTTP_200_OK)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    """delete content by content id

    Args:
        content_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("DELETE /resource/delete_content")
    content.delete_content(db, content_id)
