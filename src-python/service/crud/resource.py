from model.resource_group import ResourceItemModel, ContentModel, resource_item_tag_association
from schemas.resource_base import ResourceItemSchemaCreate
from schemas.tag_base import TagSetSchema

from sqlalchemy import func
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


def get_resource_item(db: Session, resource_item_id: int) -> ResourceItemModel | None:
    """get target resource item

    Args:
        db (Session): database session
        resource_item_id (int): target resource item id

    Returns:
        ResourceItemModel | None: query result
    """
    return db.get(ResourceItemModel, resource_item_id)


def get_resource_items_by_tags(db: Session, tags_id: TagSetSchema) -> list[ResourceItemModel]:
    """get target resource item by tags

    Args:
        db (Session): database session
        tags_id (TagSetSchema): target tags id set

    Returns:
        list[ResourceItemModel]: query result
    """
    query = db.query(ResourceItemModel)\
        .join(resource_item_tag_association,
              ResourceItemModel.id == resource_item_tag_association.c.resource_item_id)\
        .where(resource_item_tag_association.c.tag_id.in_(tags_id.tags_id))\
        .group_by(ResourceItemModel.id)\
        .having(func.count() == len(tags_id.tags_id))
    return query.all()


def delete_resource_item(db: Session, resource_item_id: int):
    """delete resource item from database by id

    Args:
        db (Session): database session
        resource_item_id (int): target resource item id
    """
    if target_resource_item := db.get(ResourceItemModel, resource_item_id):
        db.delete(target_resource_item)
        if target_contents := db.query(ContentModel).filter(
                ContentModel.resource_item_id == target_resource_item.id):
            for target_content in target_contents:
                db.delete(target_content)
        db.commit()
