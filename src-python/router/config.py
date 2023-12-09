from typing import Optional

from schemas.token import LoginSchema
from schemas.config import SystemConfigSchema, BasicConfigSchema
from service.config import system_config, basic_config
from service.security import authentication_manager
from service.logger import logger

from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/config")


@router.get("/get_config/{section}", response_model=SystemConfigSchema | BasicConfigSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_config(section: str) -> SystemConfigSchema | BasicConfigSchema:
    """get all available config to frontend

    Returns:
        SystemConfigModel | BasicConfigModel: config or error

    Raises:
        HTTPException: error response 404
    """
    logger.debug(f"GET /config/get_config/{section}")
    data: Optional[SystemConfigSchema | BasicConfigSchema] = None
    match section:
        case "system":
            data = system_config.model
        case "basic":
            data = basic_config.model
    if data is None:
        logger.warning(f"{section} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"`{section}` 查找失败")
    else:
        return data


@router.put("/set_config/{section}", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
async def set_config(section: str, value: SystemConfigSchema | BasicConfigSchema):
    """set all available config

    Args:
        section (str): section name
        value (SystemConfigModel | BasicConfigModel): new config value

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
    if (not flag):
        logger.warning(f"{section} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"`{section}`设置字段查找失败")


@router.put("/set_pwd", status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
async def set_pwd(pwd: LoginSchema):
    logger.info("PUT /config/set_pwd")
    if not authentication_manager.set_pwd(pwd.password):
        logger.error(f"password save failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="密码保存异常")
