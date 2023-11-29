from .tag_base import TagSchema
from .note_base import NoteSchema

from pydantic import ConfigDict


class TagRelationshipSchema(TagSchema):
    """full data
    """
    notes: list[NoteSchema]

    model_config = ConfigDict(from_attributes=True)
