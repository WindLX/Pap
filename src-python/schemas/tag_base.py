from pydantic import BaseModel


class TagBaseSchema(BaseModel):
    """for impl
    """
    name: str
    color: str


class TagCreateSchema(TagBaseSchema):
    """for create
    """
    note_id: int


class TagSchema(TagBaseSchema):
    """without relationship
    """
    id: int


class TagSetSchema(BaseModel):
    """from filter
    """
    tags_id: list[int]
