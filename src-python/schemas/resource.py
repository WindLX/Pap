from .resource_base import ResourceItemSchema
from .tag_base import TagSchema
from .content import ContentSchema

from pydantic import ConfigDict


class ResourceItemSchemaContent(ResourceItemSchema):
    """without tags
    """
    id: int
    contents: list[ContentSchema]

    model_config = ConfigDict(from_attributes=True)


class ResourceItemSchemaRelationship(ResourceItemSchemaContent):
    """full data
    """
    tags: list[TagSchema]
