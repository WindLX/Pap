from pydantic import BaseModel


class TagModel(BaseModel):
    name: str
    color: str
