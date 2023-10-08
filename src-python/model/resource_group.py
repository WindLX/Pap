from os import path, remove

from service.database import Base

from sqlalchemy import Column, ForeignKey, Integer, Table, String, event
from sqlalchemy.orm import relationship, Mapper
from sqlalchemy.engine import Connection

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
    contents = relationship(
        "ContentModel", back_populates="resource_item")

    def __repr__(self):
        return "<ResourceItemModel(id='%d', name='%s', url='%s')>" % self.id, self.name, self.url


@event.listens_for(ResourceItemModel, 'before_delete')
def remove_resource_item_file(_mapper: Mapper[ResourceItemModel], _connection: Connection, target: ResourceItemModel):
    """remove resource item file before delete

    Args:
        _mapper (Mapper[ResourceItem]): Mapper of ResourceItem
        _connection (Connection): database connection
        target (ResourceItem): target instance
    """
    if path.exists(target.url):
        remove(target.url)


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


@event.listens_for(ContentModel, 'after_insert')
def create_content_file(_mapper: Mapper[ContentModel], _connection: Connection, target: ContentModel):
    """create content file after insert

    Args:
        _mapper (Mapper[ContentModel]): Mapper of ContentModel
        _connection (Connection): database connection
        target (ContentModel): target instance
    """
    file = open(target.url, "w")
    file.close()


@event.listens_for(ContentModel, 'before_delete')
def remove_content_file(_mapper: Mapper[ContentModel], _connection: Connection, target: ContentModel):
    """remove content file before delete

    Args:
        _mapper (Mapper[ContentModel]): Mapper of ContentModel
        _connection (Connection): database connection
        target (ContentModel): target instance
    """
    if path.exists(target.url):
        remove(target.url)
