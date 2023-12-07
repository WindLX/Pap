from schemas.net import NetSchema
from schemas.note import NoteSchema
from model.note_group import NoteModel
from service.net import net_generator
from service.logger import logger
from service.database import get_db

from sqlalchemy.orm import Session
from fastapi import status, APIRouter, Depends

router = APIRouter(prefix="/net")


@router.get("/get_net", response_model=NetSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_net(db: Session = Depends(get_db)) -> NetSchema:
    """generate relationship net and send to frontend

    Returns:
        NetSchema: net
    """
    logger.debug(f"GET /net/get_net")
    notes = db.query(NoteModel).all()

    def parse_model(note: NoteModel) -> NoteSchema:
        n = NoteSchema(id=int(note.id), name=str(note.name), url=str(note.url))
        return n

    n_notes = list(map(lambda x: parse_model(x), notes))
    return net_generator.generate(n_notes)
