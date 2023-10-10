from pydantic import BaseModel


class TagSchemaBase(BaseModel):
    """for impl
    """
    name: str
    color: str


class TagSchemaCreate(TagSchemaBase):
    """for create
    """
    resource_item_id: int


class TagSchema(TagSchemaBase):
    """without relationship
    """
    id: int
