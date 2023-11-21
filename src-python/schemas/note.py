from __future__ import annotations
from pydantic import BaseModel, ConfigDict


class NoteSchemaBase(BaseModel):
    """for impl
    """
    name: str


class NoteSchemaCreate(NoteSchemaBase):
    """for create
    """
    pass


class NoteSchema(NoteSchemaCreate):
    """full data
    """
    id: int
    url: str

    model_config = ConfigDict(from_attributes=True)


class FolderSchemaBase(BaseModel):
    """for impl
    """
    name: str


class FolderSchemaCreate(FolderSchemaBase):
    """for create
    """
    pass


class FolderSchema(FolderSchemaCreate):
    """full data
    """
    folder: list[FolderSchema]
    note: list[NoteSchema]
