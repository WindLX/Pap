from os import path, mkdir
from shutil import rmtree, move

from service.config import path_config
from model.note import NoteModel
from schemas.note import NoteSchemaCreate, FolderSchemaCreate, FolderSchema

from sqlalchemy.orm import Session


def create_note(db: Session, note: NoteSchemaCreate) -> NoteModel:
    """create a new note to database

    Args:
        db (Session): database session
        note (NoteSchemaCreate): note schema for create

    Returns:
        NoteModel: new note
    """

    note_path = path.join(path_config.note_dir, f"{note.name}.md")
    if path.exists(note_path):
        note_path = f"{note_path}.other"
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


def delete_note(db: Session, note_id: int):
    """delete the note from database

    Args:
        db (Session): database session
        note_id (int): target note id
    """
    if target_note := db.get(NoteModel, note_id):
        db.delete(target_note)
        db.commit()


def create_folder(folder: FolderSchemaCreate) -> bool:
    """create a folder

    Args:
        folder (FolderSchemaCreate): folder schema for create

    Returns:
        bool: is successed
    """
    folder_path = path.join(path_config.note_dir, folder.name)
    if not path.exists(folder_path):
        mkdir(folder_path)
        return True
    return False


def delete_folder(folder: FolderSchema):
    """delete the folder

    Args:
        folder (FolderSchema): target folder
    """
    if path.exists(target_folder := path.join(path_config.note_dir, folder.name)):
        rmtree(target_folder)


# def move_note(db: Session, note_id: int, folder_id: int):
#     """move note to the folder

#     Args:
#         db (Session): database session
#         note_id (int): target note id
#         folder_id (int): target folder id
#     """
#     if target_note := db.get(NoteModel, note_id):
#         target_folder = db.get(FolderModel, folder_id)
#         target_folder_path = path.join(
#             path_config.note_dir, target_folder.name)
#         target_note_path = path.join(target_folder_path, target_note.name)
#         if not path.exists(target_folder_path):
#             mkdir(target_folder_path)
#         if path.exists(target_note_path):
#             raise Exception("target note already exists")
#         move(path.join(path_config.note_dir, note_id), target_note_path)
#         target_note.folder_id = folder_id
