from pydantic import BaseModel


class ResourceSchema (BaseModel):
    name: str
    url: str
