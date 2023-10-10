from model.resource_group import ResourceItemModel, ContentModel
from schemas.resource_base import ResourceItemSchemaCreate
from schemas.tag_base import TagSchema

from sqlalchemy.orm import Session


def create_resource_item(db: Session, resource_item: ResourceItemSchemaCreate) -> ResourceItemModel:
    """create a new resource item to database

    Args:
        db (Session): database session
        resource_item (ResourceItemSchemaCreate): resource item schema for create

    Returns:
        ResourceItemModel: new resource item
    """
    db_resource_item = ResourceItemModel(
        name=resource_item.name, url=resource_item.url)
    db.add(db_resource_item)
    db.commit()
    db.refresh(db_resource_item)
    return db_resource_item


def get_resource_items(db: Session) -> list[ResourceItemModel]:
    """get all resource items

    Args:
        db (Session): database session

    Returns:
        list[ResourceItemModel]: query result
    """
    return db.query(ResourceItemModel).all()


def get_resource_item(db: Session, resource_item_id: int) -> ResourceItemModel:
    """get target resource item

    Args:
        db (Session): database session
        resource_item_id (int): target resource item id

    Returns:
        ResourceItemModel: query result
    """
    return db.query(ResourceItemModel).get(resource_item_id)


def get_resource_items_by_tags(db: Session, tags: list[TagSchema]) -> list[ResourceItemModel]:
    # TODO Test
    return db.query(ResourceItemModel).filter(*list(
        filter(lambda tag: tag.id in list(
            map(lambda tag: tag.id, ResourceItemModel.tags)), tags))).all()


def delete_resource_item(db: Session, resource_item_id: int):
    """delete resource item from database by id

    Args:
        db (Session): database session
        resource_item_id (int): target resource item id
    """
    if target_resource_item := db.query(ResourceItemModel).get(resource_item_id):
        db.delete(target_resource_item)
        if target_contents := db.query(ContentModel).filter(
                ContentModel.resource_item_id == target_resource_item.id):
            for target_content in target_contents:
                db.delete(target_content)
        db.commit()
