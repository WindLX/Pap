from os import path

from model.note import NoteModel
from schemas.note import NoteSchemaCreate, NoteSchema, FolderSchema, FolderSchemaCreate
from service.config import path_config
from service.logger import logger
from service.database import get_db
from service.crud import note

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends, UploadFile

router = APIRouter(prefix="/note")


@router.post("/create_note", response_model=NoteSchema, status_code=status.HTTP_201_CREATED, include_in_schema=True)
def create_note(new_note: NoteSchemaCreate, db: Session = Depends(get_db)) -> NoteModel:
    """create a new note

    Args:
        new_note (NoteSchemaCreate): new note data
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        NoteSchema: new note data
    """
    logger.info("POST /note/create_note")
    return note.create_note(db, new_note)


@router.get("/get_notes", response_model=list[NoteSchema], status_code=status.HTTP_200_OK, include_in_schema=True)
def get_notes(db: Session = Depends(get_db)) -> list[NoteModel]:
    """get all notes

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        list[NoteModel]: all note models
    """
    logger.debug("GET /note/get_notes")
    return note.get_notes(db)


@router.get("/get_note", response_model=NoteSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteModel:
    """get note by id

    Args:
        note_id (int): note id 
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target note

    Returns:
        ContentModel: query result, note model
    """
    logger.debug("GET /note/get_note")
    if (data := note.get_note(db, note_id)):
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标笔记文件查找失败")


@router.post("/save_note", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def save_note(note_id: int, file: UploadFile, db: Session = Depends(get_db)):
    """save note by id

    Args:
        note_id (int): note id 
        file (UploadFile): upload file from frontend
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target note
    """
    logger.debug("POST /note/save_note")
    if (data := note.get_note(db, note_id)):
        file_data = file.file.read()
        file_path = path.join(path_config.note_dir, data.name)
        with open(f"{file_path}.md", 'wb') as fout:
            fout.write(file_data)
            file.file.close()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标笔记文件查找失败")


@router.delete("/delete_note", status_code=status.HTTP_200_OK, include_in_schema=True)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """delete note by note id

    Args:
        note_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("DELETE /note/delete_note")
    note.delete_note(db, note_id)


@router.post("/create_folder", status_code=status.HTTP_200_OK, include_in_schema=True)
def create_folder(new_folder: FolderSchemaCreate):
    """create folder

    Args:
        new_folder (FolderSchemaCreate): new folder schema
    """
    logger.info("POST /note/create_folder")
    if not note.create_folder(new_folder):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="文件夹创建失败")
