from os import path

from service.config import path_config
from model.resource_group import ResourceItemModel, ContentModel
from schemas.content import ContentSchemaCreate, ContentSchemaUpdate

from sqlalchemy.orm import Session
from uuid import uuid4


def create_content(db: Session, content: ContentSchemaCreate) -> ResourceItemModel | None:
    """create a new content to database

    Args:
        db (Session): database session
        content (ContentSchemaCreate): content schema for create

    Returns:
        ResourceItemModel | None: target resource item with new content, return None if target resource item doesn't exist
    """

    if (db_resource_item := db.get(ResourceItemModel, content.resource_item_id)):
        content_path = path.join(
            path_config.content_dir, f"{uuid4()}.md")
        db_content = ContentModel(
            name=content.name, url=content_path, resource_item_id=content.resource_item_id)
        db.add(db_resource_item)
        db_resource_item.contents.append(db_content)
        db.commit()
        db.refresh(db_resource_item)
        return db_resource_item
    return None


def get_content(db: Session, content_id: int) -> ContentModel | None:
    """get target content

    Args:
        db (Session): database session
        content_id (int): target content id

    Returns:
        ContentModel | None: query result
    """
    return db.get(ContentModel, content_id)


def delete_content(db: Session, content_id: int):
    """delete the content from database

    Args:
        db (Session): database session
        content_id (int): target content id
    """
    if target_content := db.get(ContentModel, content_id):
        db.delete(target_content)
        db.commit()


def update_name(db: Session, content_update: ContentSchemaUpdate) -> ContentModel | None:
    """update content name

    Args:
        db (Session): database session
        content_update (ContentSchemaUpdate): content schema for update

    Returns:
        ContentModel | None: query result
    """
    if target_content := db.get(ContentModel, content_update.id):
        db.query(ContentModel).filter(ContentModel.id == content_update.id).update({
            ContentModel.name: content_update.name
        })
        db.commit()
        db.refresh(target_content)
        return target_content
    return None
