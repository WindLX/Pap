from model.resource_group import ResourceItemModel, TagModel
from schemas.tag_base import TagSchemaCreate, TagSchema
from schemas.resource import ResourceItemSchemaRelationship
from schemas.tag import TagSchemaRelationship
from service.logger import logger
from service.database import get_db
from service.crud import tag

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends

router = APIRouter(prefix="/tag")


@router.get("/get_tags", response_model=list[TagSchemaRelationship], status_code=status.HTTP_200_OK, include_in_schema=True)
def get_tags(db: Session = Depends(get_db)) -> list[TagModel]:
    """get all tags(with relationship)

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        list[TagModel]: query result, all tags model
    """
    logger.debug("GET /tag/get_tags")
    return tag.get_tags(db)


@router.post("/create_tag", response_model=TagSchemaRelationship, status_code=status.HTTP_201_CREATED, include_in_schema=True)
def create_tag(new_tag: TagSchemaCreate, db: Session = Depends(get_db)) -> TagModel:
    """create a new tag to a resource item

    Args:
        new_tag (TagSchemaCreate): new tag data
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target resource item

    Returns:
        TagSchema: created tag item
    """
    logger.info("POST /tag/create_tag")
    if created_tag := tag.create_tag(db, new_tag):
        return created_tag
    else:
        logger.warning("fail to find target resource item")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标资源文件查找失败")


@router.put("/add_tag", response_model=ResourceItemSchemaRelationship, status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def add_tag(tag_id: int, resource_item_id: int, db: Session = Depends(get_db)) -> ResourceItemModel:
    """add a tag to a resource item

    Args:
        tag_id (int): target tag id
        resource_item_id (int): target resource item id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target resource item

    Returns:
        TagSchema: created tag item
    """
    logger.info(
        f"PUT /tag/add_tag?tag_id={tag_id}&resource_item_id={resource_item_id}")
    if updated_resource_item := tag.add_tag(db, tag_id, resource_item_id):
        return updated_resource_item
    else:
        logger.warning("fail to find target resource item or tag")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标资源文件或者标签查找失败")


@router.put("/update_tag", response_model=TagSchemaRelationship, status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def update_tag(new_tag: TagSchema, db: Session = Depends(get_db)) -> TagModel:
    """update tag data to a resource item

    Args:
        new_tag (TagSchema): new tag data with id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target tag

    Returns:
        TagSchema: updated tag item
    """
    logger.info("PUT /tag/update_tag")
    if updated_tag := tag.update_tag(db, new_tag):
        return updated_tag
    else:
        logger.warning("fail to find target tag")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标标签查找失败")


@router.delete("/delete_tag", status_code=status.HTTP_200_OK, include_in_schema=True)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """delete tag by tag id(remove all relationship)

    Args:
        tag_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info(f"DELETE /tag/delete_tag?tag_id={tag_id}")
    tag.delete_tag(db, tag_id)


@router.put("/remove_tag", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def remove_tag(tag_id: int, resource_item_id: int, db: Session = Depends(get_db)):
    """remove tag by tag id(only remove relationship)

    Args:
        tag_id (int): target id
        resource_item_id (int): related resource item id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info(
        f"PUT /tag/remove_tag?tag_id={tag_id}&resource_item_id={resource_item_id}")
    tag.remove_tag(db, tag_id, resource_item_id)
