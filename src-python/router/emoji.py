from schemas.emoji import EmojiSchema
from service.emoji import emoji_getter
from service.logger import logger

from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/emoji")


@router.get("/get_emoji", response_model=list[EmojiSchema], status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_emoji(emoji: str) -> list[EmojiSchema]:
    """search all emoji by name to frontend

    Returns:
        list[EmojiSchema]: emojis or error

    Raises:
        HTTPException: error response 404 | 406
    """
    logger.debug(f"GET /emoji/get_emoji?emoji={emoji}")
    data = emoji_getter.search(emoji)
    if data is not None:
        if len(data) == 0:
            logger.warning(f"{emoji} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"`{emoji}` 查找失败")
        else:
            return data
    else:
        logger.error(f"emoji database not found: {emoji_getter.db_path}")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"`emoji数据库加载失败")
