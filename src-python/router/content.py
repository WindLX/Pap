from schemas.resource import ResourceItemSchemaRelationship
from schemas.content import ContentSchemaCreate
from service.logger import logger
from service.database import get_db
from service.crud import content

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter, Depends

router = APIRouter(prefix="/content")


@router.post("/create_content", response_model=ResourceItemSchemaRelationship, status_code=status.HTTP_201_CREATED, include_in_schema=True)
def create_content(new_content: ContentSchemaCreate, db: Session = Depends(get_db)) -> ResourceItemSchemaRelationship:
    """create a new content to a resource item

    Args:
        new_content (ContentSchemaCreate): new content data
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 for not find the target resource item

    Returns:
        ResourceItemSchemaRelationship: updated resource item
    """
    logger.info("POST /content/create_content")
    if updated_resource_item := content.create_content(db, new_content):
        return updated_resource_item
    else:
        logger.warning("fail to find target resource item")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"目标资源文件查找失败")


@router.delete("/delete_content", status_code=status.HTTP_200_OK, include_in_schema=True)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    """delete content by content id

    Args:
        content_id (int): target id
        db (Session, optional): database session. Defaults to Depends(get_db).
    """
    logger.info("DELETE /content/delete_content")
    content.delete_content(db, content_id)
