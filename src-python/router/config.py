from typing import Optional

from model.config import BasicConfigModel, PathConfigModel
from service.config import basic_config, path_config
from service.logger import logger

from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/config",)


@router.get("/get_config/{section}", response_model=BasicConfigModel | PathConfigModel)
async def get_config(section: str):
    """get all available config to frontend

    Returns:
        BasicConfigModel | PathConfigModel: config or error

    Raises:
        HTTPException: error response 404
    """
    logger.debug(f"GET /config/get_config/{section}")
    data: Optional[BasicConfigModel | PathConfigModel] = None
    match section:
        case "basic":
            data = basic_config.model
        case "path":
            data = path_config.model
    if data is None:
        logger.warning(f"{section} not found")
        raise HTTPException(status_code=404, detail=f"{section} not found")
    else:

        return data


@router.put("/set_config/{section}", status_code=status.HTTP_202_ACCEPTED)
async def set_config(section: str, value: BasicConfigModel | PathConfigModel):
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
            if basic_config.model is not None and type(value) == BasicConfigModel:
                basic_config.model = value
            else:
                logger.warning(f"{section} not found")
                raise HTTPException(
                    status_code=404, detail=f"{section} not found")
        case "path":
            if path_config.model is not None and type(value) == PathConfigModel:
                path_config.model = value
                path_config.check_path()
            else:
                logger.warning(f"{section} not found")
                raise HTTPException(
                    status_code=404, detail=f"{section} not found")
