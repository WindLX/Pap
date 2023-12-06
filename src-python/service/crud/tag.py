from model.note_group import NoteModel, TagModel
from schemas.tag_base import TagCreateSchema, TagSchema

from sqlalchemy.orm import Session


def get_tags(db: Session) -> list[TagModel]:
    """get tags

    Args:
        db (Session): database session

    Returns:
        list[TagModel]: query result
    """
    return db.query(TagModel).all()


def get_note_tags(db: Session, note_id: int) -> list[TagModel]:
    """get target note's tags

    Args:
        db (Session): database session
        note_id (int): target note id

    Returns:
        list[TagModel]: query result
    """
    if db_note := db.get(NoteModel, note_id):
        return db_note.tags
    else:
        return []


def create_tag(db: Session, tag: TagCreateSchema) -> TagModel | None:
    """create a new tag to database

    Args:
        db (Session): database session
        tag (TagCreateSchema): tag schema for create

    Returns:
        TagModel | None: created tag, return None if target tag doesn't exist
    """

    if db_note := db.get(NoteModel, tag.note_id):
        db_tag = TagModel(name=tag.name, color=tag.color)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        db_note.tags.append(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    return None


def add_tag(db: Session, tag_id: int, note_id: int) -> NoteModel | None:
    """add a tag to target note

    Args:
        db (Session): database session
        tag_id (int): target tag id
        note_id (int): target note id

    Returns:
        NoteModel | None: updated note, return None if target tag or note doesn't exist
    """

    if (db_note := db.get(NoteModel, note_id)) and (db_tag := db.get(TagModel, tag_id)):
        db_note.tags.append(db_tag)
        db.commit()
        db.refresh(db_note)
        return db_note
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
        db.refresh(db_tag)
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


def remove_tag(db: Session, tag_id: int, note_id: int):
    """remove the tag in the tag

    Args:
        db (Session): database session
        tag_id (int): target tag id
        note_id (int): target tag id
    """
    if (db_note := db.get(NoteModel, note_id)) and ((db_tag := db.get(TagModel, tag_id))):
        db_note.tags.remove(db_tag)
        db.commit()
    return None


def remove_note(db: Session, tag_id: int, note_id: int):
    """remove the note in the tag

    Args:
        db (Session): database session
        tag_id (int): target tag id
        note_id (int): target tag id
    """
    if (db_note := db.get(NoteModel, note_id)) and ((db_tag := db.get(TagModel, tag_id))):
        db_tag.notes.remove(db_note)
        db.commit()
    return None
