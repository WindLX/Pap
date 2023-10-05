from pydantic import BaseModel


class TagSchemaBase(BaseModel):
    """for impl
    """
    name: str
    color: str


class TagSchemaCreate(TagSchemaBase):
    """for create
    """
    pass


class TagSchema(TagSchemaCreate):
    """without relationship
    """
    id: int
