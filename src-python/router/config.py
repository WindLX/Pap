from typing import Optional

from schemas.config import SystemConfigSchema, BasicConfigSchema, PathConfigSchema
from service.config import system_config, basic_config, path_config
from service.logger import logger

from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/config")


@router.get("/get_config/{section}", response_model=SystemConfigSchema | BasicConfigSchema | PathConfigSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_config(section: str) -> SystemConfigSchema | BasicConfigSchema | PathConfigSchema:
    """get all available config to frontend

    Returns:
        SystemConfigModel | BasicConfigModel | PathConfigModel: config or error

    Raises:
        HTTPException: error response 404
    """
    logger.debug(f"GET /config/get_config/{section}")
    data: Optional[SystemConfigSchema |
                   BasicConfigSchema | PathConfigSchema] = None
    match section:
        case "system":
            data = system_config.model
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
async def set_config(section: str, value: SystemConfigSchema | BasicConfigSchema | PathConfigSchema):
    """set all available config

    Args:
        section (str): section name
        value (SystemConfigModel | BasicConfigModel | PathConfigModel): new config value

    Raises:
        HTTPException: error response 404
    """
    logger.info(f"PUT /config/set_config/{section}")
    flag = True
    match section:
        case "system":
            if system_config.model is not None and type(value) == SystemConfigSchema:
                system_config.model = value
            else:
                flag = False
        case "basic":
            if basic_config.model is not None and type(value) == BasicConfigSchema:
                basic_config.model = value
            else:
                flag = False
        case "path":
            if path_config.model is not None and type(value) == PathConfigSchema:
                path_config.model = value
                path_config.check_path()
            else:
                flag = False
    if (not flag):
        logger.warning(f"{section} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"`{section}` 查找失败")
