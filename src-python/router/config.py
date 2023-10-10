from typing import Optional

from schemas.config import BasicConfigSchema, PathConfigSchema
from service.config import basic_config, path_config
from service.logger import logger

from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/config")


@router.get("/get_config/{section}", response_model=BasicConfigSchema | PathConfigSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_config(section: str) -> BasicConfigSchema | PathConfigSchema:
    """get all available config to frontend

    Returns:
        BasicConfigModel | PathConfigModel: config or error

    Raises:
        HTTPException: error response 404
    """
    logger.debug(f"GET /config/get_config/{section}")
    data: Optional[BasicConfigSchema | PathConfigSchema] = None
    match section:
        case "basic":
            data = basic_config.model
        case "path":
            data = path_config.model
    if data is None:
        logger.warning(f"{section} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"`{section}` 查找失败")
    else:

        return data


@router.put("/set_config/{section}", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
async def set_config(section: str, value: BasicConfigSchema | PathConfigSchema):
    """set all available config

    Args:
        section (str): section name
        value (BasicConfigModel | PathConfigModel): new config value

    Raises:
        HTTPException: error response 404
    """
    logger.info(f"PUT /config/set_config/{section}")
    match section:
        case "basic":
            if basic_config.model is not None and type(value) == BasicConfigSchema:
                basic_config.model = value
            else:
                logger.warning(f"{section} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"`{section}` 查找失败")
        case "path":
            if path_config.model is not None and type(value) == PathConfigSchema:
                path_config.model = value
                path_config.check_path()
            else:
                logger.warning(f"{section} not found")
                raise HTTPException(
                    status_code=404, detail=f"`{section}` 查找失败")
