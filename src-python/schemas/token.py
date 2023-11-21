from pydantic import BaseModel


class LoginSchema(BaseModel):
    """Login
    """
    password: str


class TokenSchema(BaseModel):
    """Token
    """
    access_token: str
    token_type: str
