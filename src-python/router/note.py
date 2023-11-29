from model.note import NoteModel
from schemas.note import NoteSchemaCreate, NoteSchema, NoteSchemaUpdate
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
    logger.debug(f"GET /note/get_note?note_id={note_id}")
    if (data := note.get_note(db, note_id)):
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标笔记文件查找失败")


@router.get("/get_note_by_name", response_model=NoteSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
def get_note_by_name(note_name: str, index: int, db: Session = Depends(get_db)) -> NoteModel:
    """get note by name

    Args:
        note_name (str): note name
        index (int): index
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target note

    Returns:
        ContentModel: query result, note model
    """
    logger.debug(
        f"GET /note/get_note_by_name?note_name={note_name}&index={index}")
    if (data := note.get_note_by_name(db, note_name, index)):
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
    logger.debug(f"POST /note/save_note?note_id={note_id}")
    if (data := note.get_note(db, note_id)):
        file_data = file.file.read()
        with open(data.url, 'wb') as fout:
            fout.write(file_data)
            file.file.close()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标笔记文件查找失败")


@router.put("/rename_note", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def rename_note(note_update: NoteSchemaUpdate, db: Session = Depends(get_db)):
    """update note name

    Args:
        note_update (NoteSchemaUpdate): update note data
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("PUT /note/rename_note")
    note.update_name(db, note_update)


@router.delete("/delete_note", status_code=status.HTTP_200_OK, include_in_schema=True)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """delete note by note id

    Args:
        note_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info(f"DELETE /note/delete_note?note_id={note_id}")
    note.delete_note(db, note_id)
