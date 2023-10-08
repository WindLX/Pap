from os import path

from service.config import path_config
from model.resource_group import ResourceItemModel, ContentModel
from schemas.content import ContentSchemaCreate

from sqlalchemy.orm import Session


def create_content(db: Session, content: ContentSchemaCreate) -> ResourceItemModel | None:
    """create a new content to database

    Args:
        db (Session): database session
        content (ContentSchemaCreate): content schema for create

    Returns:
        ResourceItemModel | None: target resource item with new content, return None if target resource item doesn't exist
    """

    if (db_resource_item := db.query(ResourceItemModel).filter(
            ResourceItemModel.id == content.resource_item_id).first()):
        content_path = path.join(path_config.content_dir, f"{content.name}.md")
        db_content = ContentModel(
            name=content.name, url=content_path, resource_item_id=content.resource_item_id)
        db.add(db_resource_item)
        db_resource_item.contents.append(db_content)
        db.commit()
        db.refresh(db_resource_item)
        return db_resource_item
    return None


def delete_content(db: Session, content_id: int):
    """delete the content from database

    Args:
        db (Session): database session
        content_id (int): target content id
    """
    if target_contents := db.query(ContentModel).filter(
            ContentModel.id == content_id):
        for target_content in target_contents:
            db.delete(target_content)
        db.commit()
