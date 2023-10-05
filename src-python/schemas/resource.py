from pydantic import BaseModel

from .tag import TagModel


class ResourceItemModel(BaseModel):
    name: str
    url: str
    tag: list[TagModel]
    content: list[str]
