from model.resource_group import ResourceItemModel
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
        db (Session): _description_

    Returns:
        list[ResourceItemModel]: _description_
    """
    return db.query(ResourceItemModel).all()


def get_resource_items_by_tags(db: Session, tags: list[TagSchema]) -> list[ResourceItemModel]:
    pass
