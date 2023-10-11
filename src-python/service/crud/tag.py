from model.resource_group import ResourceItemModel, TagModel
from schemas.tag_base import TagSchemaCreate, TagSchema

from sqlalchemy.orm import Session


def get_tags(db: Session) -> list[TagModel]:
    """get tags

    Args:
        db (Session): database session

    Returns:
        list[TagModel]: query result
    """
    return db.query(TagModel).all()


def create_tag(db: Session, tag: TagSchemaCreate) -> TagModel | None:
    """create a new tag to database

    Args:
        db (Session): database session
        tag (TagSchemaCreate): tag schema for create

    Returns:
        TagModel | None: created tag, return None if target tag doesn't exist
    """

    if db_resource_item := db.get(ResourceItemModel, tag.resource_item_id):
        db_tag = TagModel(name=tag.name, color=tag.color)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        db_resource_item.tags.append(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    return None


def add_tag(db: Session, tag_id: int, resource_item_id: int) -> ResourceItemModel | None:
    """add a tag to target resource item

    Args:
        db (Session): database session
        tag_id (int): target tag id
        resource_item_id (int): target resource item id

    Returns:
        ResourceItemModel | None: updated resource item, return None if target tag or resource item doesn't exist
    """

    if (db_resource_item := db.get(ResourceItemModel, resource_item_id)) and (db_tag := db.get(TagModel, tag_id)):
        db_resource_item.tags.append(db_tag)
        db.commit()
        db.refresh(db_resource_item)
        return db_resource_item
    return None


def update_tag(db: Session, tag: TagSchema) -> TagModel | None:
    """update tag to database

    Args:
        db (Session): database session
        tag (TagSchema): tag schema for update

    Returns:
        TagModel | None: created tag, return None if target tag doesn't exist
    """
    if db_tag := db.get(TagModel, tag.id):
        db.query(TagModel).filter(
            TagModel.id == tag.id).update({
                TagModel.name: tag.name,
                TagModel.color: tag.color
            })
        db.commit()
        return db_tag
    return None


def delete_tag(db: Session, tag_id: int):
    """delete the tag from database

    Args:
        db (Session): database session
        tag_id (int): target tag id
    """
    if target_content := db.get(TagModel, tag_id):
        db.delete(target_content)
        db.commit()


def remove_tag(db: Session, tag_id: int, resource_item_id: int):
    """remove the tag in the tag

    Args:
        db (Session): database session
        tag_id (int): target tag id
        resource_item_id (int): target tag id
    """
    if (db_resource_item := db.get(ResourceItemModel, resource_item_id)) and ((db_tag := db.get(TagModel, tag_id))):
        db_resource_item.tags.remove(db_tag)
        db.commit()
    return None


def remove_resource_item(db: Session, tag_id: int, resource_item_id: int):
    """remove the resource item in the tag

    Args:
        db (Session): database session
        tag_id (int): target tag id
        resource_item_id (int): target tag id
    """
    if (db_resource_item := db.get(ResourceItemModel, resource_item_id)) and ((db_tag := db.get(TagModel, tag_id))):
        db_tag.resource_items.remove(db_resource_item)
        db.commit()
    return None
