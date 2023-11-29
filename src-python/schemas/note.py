from pydantic import BaseModel, ConfigDict


class NoteSchemaBase(BaseModel):
    """for impl
    """
    name: str


class NoteSchemaCreate(NoteSchemaBase):
    """for create
    """
    pass


class NoteSchemaUpdate(NoteSchemaBase):
    """for update
    """
    id: int


class NoteSchema(NoteSchemaCreate):
    """full data
    """
    id: int
    url: str

    model_config = ConfigDict(from_attributes=True)
