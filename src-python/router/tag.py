from model.note_group import NoteModel, TagModel
from schemas.tag_base import TagCreateSchema, TagSchema
from schemas.note import NoteRelationshipSchema
from schemas.tag import TagRelationshipSchema
from service.logger import logger
from service.database import get_db
from service.crud import tag

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends

router = APIRouter(prefix="/tag")


@router.get("/get_tags", response_model=list[TagRelationshipSchema], status_code=status.HTTP_200_OK, include_in_schema=True)
def get_tags(db: Session = Depends(get_db)) -> list[TagModel]:
    """get all tags(with relationship)

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        list[TagModel]: query result, all tags model
    """
    logger.debug("GET /tag/get_tags")
    return tag.get_tags(db)


@router.post("/create_tag", response_model=TagRelationshipSchema, status_code=status.HTTP_201_CREATED, include_in_schema=True)
def create_tag(new_tag: TagCreateSchema, db: Session = Depends(get_db)) -> TagModel:
    """create a new tag to a note

    Args:
        new_tag (TagCreateSchema): new tag data
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target note

    Returns:
        TagSchema: created tag item
    """
    logger.info("POST /tag/create_tag")
    if created_tag := tag.create_tag(db, new_tag):
        return created_tag
    else:
        logger.warning("fail to find target note")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标笔记查找失败")


@router.put("/add_tag", response_model=NoteRelationshipSchema, status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def add_tag(tag_id: int, note_id: int, db: Session = Depends(get_db)) -> NoteModel:
    """add a tag to a note

    Args:
        tag_id (int): target tag id
        note_id (int): target note id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target note

    Returns:
        TagSchema: created tag item
    """
    logger.info(
        f"PUT /tag/add_tag?tag_id={tag_id}&note_id={note_id}")
    if updated_note := tag.add_tag(db, tag_id, note_id):
        return updated_note
    else:
        logger.warning("fail to find target note or tag")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标笔记或者标签查找失败")


@router.put("/update_tag", response_model=TagRelationshipSchema, status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def update_tag(new_tag: TagSchema, db: Session = Depends(get_db)) -> TagModel:
    """update tag data to a note

    Args:
        new_tag (TagSchema): new tag data with id
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target tag

    Returns:
        TagSchema: updated tag item
    """
    logger.info("PUT /tag/update_tag")
    if updated_tag := tag.update_tag(db, new_tag):
        return updated_tag
    else:
        logger.warning("fail to find target tag")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="目标标签查找失败")


@router.delete("/delete_tag", status_code=status.HTTP_200_OK, include_in_schema=True)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """delete tag by tag id(remove all relationship)

    Args:
        tag_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info(f"DELETE /tag/delete_tag?tag_id={tag_id}")
    tag.delete_tag(db, tag_id)


@router.put("/remove_tag", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
def remove_tag(tag_id: int, note_id: int, db: Session = Depends(get_db)):
    """remove tag by tag id(only remove relationship)

    Args:
        tag_id (int): target id
        note_id (int): related note id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info(
        f"PUT /tag/remove_tag?tag_id={tag_id}&note_id={note_id}")
    tag.remove_tag(db, tag_id, note_id)
