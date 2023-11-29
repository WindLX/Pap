from os import path
from typing import Union
from datetime import datetime, timedelta

from fastapi import status, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "dfdd202b4e5edfd0825f45718d15884224d8ea09cb7a3a253f0d4362e3132fc7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
PWD_PATH = "./data/pwd"


class AuthenticationManager:
    @staticmethod
    def get_pwd() -> str | None:
        pwd = PWD_PATH
        if not path.exists(pwd):
            with open(pwd, 'w') as f:
                f.write(get_password_hash(""))
        try:
            with open(pwd, "r") as f:
                return f.read()
        except:
            return None

    @staticmethod
    def set_pwd(new_pwd: str) -> bool:
        pwd = PWD_PATH
        try:
            with open(pwd, "w") as f:
                f.write(get_password_hash(new_pwd))
        except Exception:
            return False
        return True

    @staticmethod
    def authenticate(input_password: str):
        password = AuthenticationManager.get_pwd()
        if password is None:
            return False
        if not pwd_context.verify(input_password, password):
            return False
        return True

    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def check_jwt_token(token: str = Depends(oauth2_scheme)) -> Response | None:
        credentials_exception = Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            subject = payload.get("sub")
            expire = payload.get("exp")
            assert type(expire) == int
            if datetime.fromtimestamp(expire) < datetime.utcnow() or subject != "login":
                return credentials_exception
        except JWTError:
            return credentials_exception
        return None


def get_password_hash(password):
    return pwd_context.hash(password)


authentication_manager = AuthenticationManager()
