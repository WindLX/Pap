from typing import Optional

from schemas.config import BasicConfigSchema, PathConfigSchema
from service.config import basic_config, path_config
from service.logger import logger

from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/search")
