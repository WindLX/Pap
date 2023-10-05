from service.database import Base

from sqlalchemy import Column, ForeignKey, Integer, Table, String
from sqlalchemy.orm import relationship

resource_item_tag_association = Table(
    'resource_item_tag_association',
    Base.metadata,
    Column('resource_item_id', Integer, ForeignKey('resource_items.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class ResourceItemModel(Base):
    """resource item ORM model

    Relationships:
        tags: TagModel 'many to many'
        contents: ContentModel 'many to one'
    """
    __tablename__ = "resource_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)

    tags = relationship(
        "TagModel", secondary="resource_item_tag_association", back_populates="resource_items")
    contents = relationship("ContentModel", back_populates="resource_item")

    def __repr__(self):
        return "<ResourceItemModel(id='%d', name='%s', url='%s')>" % self.id, self.name, self.url


class TagModel(Base):
    """tag ORM model

    Relationships:
        resource_items: ResourceItemModel 'many to many'
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=15))
    color = Column(String(length=7))

    resource_items = relationship(
        "ResourceItemModel", secondary="resource_item_tag_association", back_populates="tags")

    def __repr__(self):
        return "<TagModel(id='%d', name='%s', color='%s')>" % self.id, self.name, self.color


class ContentModel(Base):
    """content ORM model

    Relationships:
        resource_item: ResourceItemModel 'one to many'
    """
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=15))
    url = Column(String)

    resource_item_id = Column(Integer, ForeignKey('resource_items.id'))
    resource_item = relationship(
        "ResourceItemModel", back_populates="contents")

    def __repr__(self):
        return "<ContentModel(id='%d', name='%s', url='%s')>" % self.id, self.name, self.url
