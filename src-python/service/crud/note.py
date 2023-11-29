from os import path

from service.config import path_config
from model.note import NoteModel
from schemas.note import NoteSchemaCreate, NoteSchemaUpdate

from sqlalchemy.orm import Session
from uuid import uuid4


def create_note(db: Session, note: NoteSchemaCreate) -> NoteModel:
    """create a new note to database

    Args:
        db (Session): database session
        note (NoteSchemaCreate): note schema for create

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


def get_note_by_name(db: Session, note_name: str, index: int) -> NoteModel | None:
    """get target note by name

    Args:
        db (Session): database session
        note_name (str): target note name
        index (int): index

    Returns:
        NoteModel | None: query result
    """
    notes = db.query(NoteModel).filter(NoteModel.name == note_name).all()
    if index < len(notes) and index >= 0:
        return notes[index]
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


def update_name(db: Session, note_update: NoteSchemaUpdate) -> NoteModel | None:
    """update note name

    Args:
        db (Session): database session
        note_update (NoteSchemaUpdate): note schema for update

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
