from schemas.net import NetSchema
from model.note_group import NoteModel
from service.net import net_generator
from service.logger import logger
from service.database import get_db

from fastapi import status, APIRouter, Depends

router = APIRouter(prefix="/net")


@router.get("/get_net", response_model=NetSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_net(db: Depends(get_db)) -> NetSchema:
    """generate relationship net and send to frontend

    Returns:
        NetSchema: net
    """
    logger.debug(f"GET /net/get_net")
    notes = db.query(NoteModel).all()
    return net_generator.generate(notes)
