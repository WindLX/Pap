from .tag_base import TagSchema
from .resource_base import ResourceItemSchema

from pydantic import ConfigDict


class TagSchemaRelationship(TagSchema):
    """full data
    """
    resources: list[ResourceItemSchema]

    model_config = ConfigDict(from_attributes=True)
