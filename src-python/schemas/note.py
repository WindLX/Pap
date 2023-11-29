from .note_base import NoteSchema
from .tag_base import TagSchema

from pydantic import ConfigDict


class NoteRelationshipSchema(NoteSchema):
    """full data
    """
    tags: list[TagSchema]

    model_config = ConfigDict(from_attributes=True)
