from os import path

from service.config import path_config
from model.note_group import NoteModel, note_tag_association
from schemas.note_base import NoteCreateSchema, NoteUpdateSchema
from schemas.tag_base import TagSetSchema

from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import uuid4


def create_note(db: Session, note: NoteCreateSchema) -> NoteModel:
    """create a new note to database

    Args:
        db (Session): database session
        note (NoteCreateSchema): note schema for create

    Returns:
        NoteModel: new note
    """
    note_path = path.join(path_config.note_dir, f"{uuid4()}.md")
    db_note = NoteModel(name=note.name, url=note_path)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes(db: Session) -> list[NoteModel]:
    """get all notes

    Args:
        db (Session): database session

    Returns:
        list[NoteModel]: query result
    """
    return db.query(NoteModel).all()


def get_note(db: Session, note_id: int) -> NoteModel | None:
    """get target note

    Args:
        db (Session): database session
        note_id (int): target note id

    Returns:
        NoteModel | None: query result
    """
    return db.get(NoteModel, note_id)


def get_notes_by_tags(db: Session, tags_id: TagSetSchema) -> list[NoteModel]:
    """get target notes by tags

    Args:
        db (Session): database session
        tags_id (TagSetSchema): target tags id set

    Returns:
        list[NoteModel]: query result
    """
    query = db.query(NoteModel)\
        .join(note_tag_association,
              NoteModel.id == note_tag_association.c.note_id)\
        .where(note_tag_association.c.tag_id.in_(tags_id.tags_id))\
        .group_by(NoteModel.id)\
        .having(func.count() == len(tags_id.tags_id))
    return query.all()


def get_note_by_name(db: Session, note_name: str) -> NoteModel | None:
    """get target note by name

    Args:
        db (Session): database session
        note_name (str): target note name

    Returns:
        NoteModel | None: query result
    """
    if notes := db.query(NoteModel).filter(NoteModel.name == note_name).all():
        return notes[0]
    else:
        return None


def delete_note(db: Session, note_id: int):
    """delete the note from database

    Args:
        db (Session): database session
        note_id (int): target note id
    """
    if target_note := db.get(NoteModel, note_id):
        db.delete(target_note)
        db.commit()


def update_name(db: Session, note_update: NoteUpdateSchema) -> NoteModel | None:
    """update note name

    Args:
        db (Session): database session
        note_update (NoteUpdateSchema): note schema for update

    Returns:
        NoteModel | None: query result
    """
    if target_note := db.get(NoteModel, note_update.id):
        db.query(NoteModel).filter(NoteModel.id == note_update.id).update({
            NoteModel.name: note_update.name
        })
        db.commit()
        db.refresh(target_note)
        return target_note
    return None
