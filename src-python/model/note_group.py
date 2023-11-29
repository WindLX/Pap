from os import path, remove

from service.database import Base

from sqlalchemy import Column, Integer, String, Table, ForeignKey, event
from sqlalchemy.orm import relationship, Mapper
from sqlalchemy.engine import Connection


note_tag_association = Table(
    'note_tag_association',
    Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class NoteModel(Base):
    """note ORM model
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)

    tags = relationship(
        "TagModel", secondary="note_tag_association", back_populates="notes")

    def __repr__(self):
        return "<Note(id='%d', name='%s', url='%s')>" % self.id, self.name, self.url


@event.listens_for(NoteModel, 'after_insert')
def create_note_file(_mapper: Mapper[NoteModel], _connection: Connection, target: NoteModel):
    """create note file after insert

    Args:
        _mapper (Mapper[NoteModel]): Mapper of NoteModel
        _connection (Connection): database connection
        target (NoteModel): target instance
    """
    file = open(target.url, "w")
    file.close()


@event.listens_for(NoteModel, 'before_delete')
def remove_note_file(_mapper: Mapper[NoteModel], _connection: Connection, target: NoteModel):
    """remove note file before delete

    Args:
        _mapper (Mapper[NoteModel]): Mapper of NoteModel
        _connection (Connection): database connection
        target (NoteModel): target instance
    """
    if path.exists(target.url):
        remove(target.url)


class TagModel(Base):
    """tag ORM model

    Relationships:
        notes: NoteModel 'many to many'
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=15))
    color = Column(String(length=7))

    notes = relationship(
        "NoteModel", secondary="note_tag_association", back_populates="tags")

    def __repr__(self):
        return "<TagModel(id='%d', name='%s', color='%s')>" % self.id, self.name, self.color
