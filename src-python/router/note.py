from model.note_group import NoteModel
from schemas.note_base import NoteCreateSchema, NoteUpdateSchema
from schemas.note import NoteRelationshipSchema
from schemas.tag_base import TagSetSchema
from service.logger import logger
from service.database import get_db
from service.crud import note, tag

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends, UploadFile

router = APIRouter(prefix="/note")


@router.post("/create_note", response_model=NoteRelationshipSchema, status_code=status.HTTP_201_CREATED, include_in_schema=True)
def create_note(new_note: NoteCreateSchema, db: Session = Depends(get_db)) -> NoteModel:
    """create a new note

    Args:
        new_note (NoteCreateSchema): new note data
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        NoteModel: new note data
    """
    logger.info("POST /note/create_note")
    return note.create_note(db, new_note)


@router.get("/get_notes", response_model=list[NoteRelationshipSchema], status_code=status.HTTP_200_OK, include_in_schema=True)
def get_notes(db: Session = Depends(get_db)) -> list[NoteModel]:
    """get all notes

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        list[NoteModel]: all note models
    """
    logger.debug("GET /note/get_notes")
    return note.get_notes(db)


@router.get("/get_note", response_model=NoteRelationshipSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteModel:
    """get note by id

    Args:
        note_id (int): note id 
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target note

    Returns:
        NoteModel: query result, note model
    """
    logger.debug(f"GET /note/get_note?note_id={note_id}")
    if (data := note.get_note(db, note_id)):
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标笔记文件查找失败")


@router.post("/get_note_by_tags", response_model=list[NoteRelationshipSchema], status_code=status.HTTP_200_OK, include_in_schema=True)
def get_note_by_tags(tags_id: TagSetSchema, db: Session = Depends(get_db)) -> list[NoteModel]:
    """get notes by tags

    Args:
        tags_id (TagSetSchema): id of filter tags
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        list[NoteModel]: query result, all notes model
    """
    logger.debug(f"GET /note/get_note_tags?tags_id={tags_id}")
    return note.get_notes_by_tags(db, tags_id)


@router.get("/get_note_by_name", response_model=NoteRelationshipSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
def get_note_by_name(note_name: str, index: int, db: Session = Depends(get_db)) -> NoteModel:
    """get note by name

    Args:
        note_name (str): note name
        index (int): index
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target note

    Returns:
        NoteModel: query result, note model
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
def rename_note(note_update: NoteUpdateSchema, db: Session = Depends(get_db)):
    """update note name

    Args:
        note_update (NoteUpdateSchema): update note data
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


@router.put("/remove_note", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def remove_note(tag_id: int, note_id: int, db: Session = Depends(get_db)):
    """remove note by note id(only remove relationship)

    Args:
        tag_id (int): related tag id
        note_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info(
        f"PUT /note/remove_note?tag_id={tag_id}&note_id={note_id}")
    tag.remove_note(db, tag_id, note_id)
