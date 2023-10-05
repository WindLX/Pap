from .resource_base import ResourceItemSchema

from pydantic import BaseModel, ConfigDict


class ContentSchemaBase(BaseModel):
    """for impl
    """
    name: str
    url: str


class ContentSchemaCreate(ContentSchemaBase):
    """for create
    """
    pass


class ContentSchema(ContentSchemaCreate):
    """full data
    """
    id: int
    resource_item: ResourceItemSchema

    model_config = ConfigDict(from_attributes=True)
