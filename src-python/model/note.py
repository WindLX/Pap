from os import path, remove

from service.database import Base

from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import Mapper
from sqlalchemy.engine import Connection


class NoteModel(Base):
    """note ORM model
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)

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
