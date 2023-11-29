from pydantic import BaseModel


class NoteBaseSchema(BaseModel):
    """for impl
    """
    name: str


class NoteCreateSchema(NoteBaseSchema):
    """for create
    """
    pass


class NoteUpdateSchema(NoteBaseSchema):
    """for update
    """
    id: int


class NoteSchema(NoteCreateSchema):
    """without tags
    """
    id: int
    url: str
