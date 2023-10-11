from os import path

from model.resource_group import ResourceItemModel
from schemas.resource_base import ResourceItemSchemaCreate
from schemas.resource import ResourceItemSchemaRelationship
from schemas.tag_base import TagSetSchema
from service.config import path_config
from service.logger import logger
from service.database import get_db
from service.crud import resource, tag

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends, UploadFile

router = APIRouter(prefix="/resource")


@router.post("/create_resource_item", status_code=status.HTTP_201_CREATED, include_in_schema=True)
def create_resource(file: UploadFile, db: Session = Depends(get_db)):
    """create a new resource item from upload file

    Args:
        file (UploadFile): upload file from frontend
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: error response 403
    """
    logger.info("POST /resource/create_resource_item")
    if (raw_filename := file.filename) is not None:
        file_name, file_extension = path.splitext(raw_filename)
        if file_extension == ".pdf":
            file_data = file.file.read()
            assert file_name is not None
            file_path = path.join(path_config.resource_dir, raw_filename)
            with open(file_path, 'wb') as fout:
                fout.write(file_data)
                file.file.close()
            resource_item = ResourceItemSchemaCreate(
                name=file_name, url=file_path)
            resource.create_resource_item(db, resource_item=resource_item)
        else:
            logger.warning("invalid file extension")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"`{file_extension}` 无效的文件后缀")
    else:
        logger.warning("invalid file name")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"不存在的文件名")


@router.get("/get_resource", response_model=list[ResourceItemSchemaRelationship], status_code=status.HTTP_200_OK, include_in_schema=True)
def get_resource(db: Session = Depends(get_db)) -> list[ResourceItemModel]:
    """get all resource items

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        list[ResourceItemModel]: query result, all resource items model
    """
    logger.debug("GET /resource/get_resource")
    return resource.get_resource_items(db)


@router.post("/get_resource_by_tags", response_model=list[ResourceItemSchemaRelationship], status_code=status.HTTP_200_OK, include_in_schema=True)
def get_resource_by_tags(tags_id: TagSetSchema, db: Session = Depends(get_db)) -> list[ResourceItemModel]:
    """get resource items by tags

    Args:
        tags_id (TagSetSchema): id of filter tags
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        list[ResourceItemModel]: query result, all resource items model
    """
    logger.debug("GET /resource/get_resource_by_tags")
    return resource.get_resource_items_by_tags(db, tags_id)


@router.get("/get_resource_item", response_model=ResourceItemSchemaRelationship, status_code=status.HTTP_200_OK, include_in_schema=True)
def get_resource_item(resource_item_id: int, db: Session = Depends(get_db)) -> ResourceItemModel:
    """get target resource item (with relationship)

    Args:
        resource_item_id (int): target resource item id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target resource item

    Returns:
        ResourceItemModel: query result
    """
    logger.debug("GET /resource/get_resource_item")
    if (data := resource.get_resource_item(db, resource_item_id)):
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标资源文件查找失败")


@router.delete("/delete_resource_item", status_code=status.HTTP_200_OK, include_in_schema=True)
def delete_resource_item(resource_item_id: int, db: Session = Depends(get_db)):
    """delete resource item by resource item id

    Args:
        resource_item_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("DELETE /resource/delete_resource_item")
    resource.delete_resource_item(db, resource_item_id)


@router.put("/remove_resource_item", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def remove_resource_item(tag_id: int, resource_item_id: int, db: Session = Depends(get_db)):
    """remove resource item by resource item id(only remove relationship)

    Args:
        tag_id (int): related tag id
        resource_item_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("PUT /resource/remove_resource_item")
    tag.remove_resource_item(db, tag_id, resource_item_id)
