from schemas.token import TokenSchema, LoginSchema
from service.logger import logger
from service.security import authentication_manager

from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/login")


@router.post("/", response_model=TokenSchema, status_code=status.HTTP_200_OK, include_in_schema=True)
async def login(login: LoginSchema):
    logger.info("POST /login")
    result = authentication_manager.authenticate(login.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = authentication_manager.create_access_token(
        data={"sub": "login"}
    )
    return TokenSchema(access_token=access_token, token_type="bearer")
