from pydantic import BaseModel


class ResourceItemSchemaBase(BaseModel):
    """for impl
    """
    name: str
    url: str


class ResourceItemSchemaCreate(ResourceItemSchemaBase):
    """for create
    """
    pass


class ResourceItemSchema(ResourceItemSchemaCreate):
    """without tags && contents
    """
    id: int
