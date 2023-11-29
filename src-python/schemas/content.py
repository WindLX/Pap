from pydantic import BaseModel, ConfigDict


class ContentSchemaBase(BaseModel):
    """for impl
    """
    name: str


class ContentSchemaCreate(ContentSchemaBase):
    """for create
    """
    resource_item_id: int


class ContentSchemaUpdate(ContentSchemaBase):
    """for update
    """
    id: int


class ContentSchema(ContentSchemaCreate):
    """full data
    """
    id: int
    url: str

    model_config = ConfigDict(from_attributes=True)
