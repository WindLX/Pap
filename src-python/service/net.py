from schemas.net import NetLinkSchema, NetNodeSchema, NetSchema
from schemas.note import NoteSchema


class NetGenerator:
    """
    Generate net schema
    """

    def __init__(self):
        pass

    def generate(self, notes: list[NoteSchema]) -> NetSchema:
        for note in notes:
            with open(note.url, 'r') as f:
                


net_generator = NetGenerator()
