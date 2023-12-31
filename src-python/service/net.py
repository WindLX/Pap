import ctypes
from sys import platform

from schemas.note import NoteSchema
from schemas.net import NetSchema, NetNodeSchema, NetLinkSchema, Vector

if platform.startswith('linux'):
    lib_name = 'libmd_net.so'
elif platform.startswith('win'):
    lib_name = 'md_net.dll'
else:
    raise Exception('Unknown platform')
lib = ctypes.CDLL(f"./{lib_name}")


class CNoteSchema(ctypes.Structure):
    _fields_ = [("id", ctypes.c_uint32),
                ("name", ctypes.POINTER(ctypes.c_char)),
                ("url", ctypes.POINTER(ctypes.c_char))]


class CNoteSchemaVec(ctypes.Structure):
    _fields_ = [("notes", ctypes.POINTER(CNoteSchema)),
                ("len", ctypes.c_uint32)]


class CNetNodeSchema(ctypes.Structure):
    _fields_ = [("id", ctypes.c_uint32),
                ("data", ctypes.c_char_p),
                ("is_md", ctypes.c_uint32),
                ("pos_x", ctypes.c_uint32),
                ("pos_y", ctypes.c_uint32)]


class CNetLinkSchema(ctypes.Structure):
    _fields_ = [("source", ctypes.c_uint32),
                ("target", ctypes.c_uint32)]


class CNetSchema(ctypes.Structure):
    _fields_ = [("nodes", ctypes.POINTER(ctypes.POINTER(CNetNodeSchema))),
                ("n_len", ctypes.c_uint),
                ("links", ctypes.POINTER(ctypes.POINTER(CNetLinkSchema))),
                ("l_len", ctypes.c_uint)]


class CNetGenerator(ctypes.Structure):
    _fields_ = [("gen", ctypes.c_void_p)]


init_net_generator = lib.init_net_generator
init_net_generator.restype = ctypes.POINTER(CNetGenerator)

generate = lib.generate
generate.argtypes = [ctypes.POINTER(
    CNetGenerator), ctypes.POINTER(CNoteSchemaVec)]
generate.restype = ctypes.POINTER(CNetSchema)

free_net_schema = lib.free_net_schema
free_net_schema.argtypes = [ctypes.POINTER(CNetSchema)]


class NetGenerator:
    def __init__(self):
        self.generator = init_net_generator()

    def generate(self, notes: list[NoteSchema]) -> NetSchema:
        cnotes = copy_notes(notes)
        cnet = generate(self.generator, ctypes.byref(cnotes))
        net = parse_cnet(cnet.contents)
        free_net_schema(cnet)
        return net

    def __del__(self):
        pass


def copy_note(note: NoteSchema) -> CNoteSchema:
    c_note = CNoteSchema()
    c_note.id = note.id
    c_note.name = ctypes.create_string_buffer(note.name.encode('utf-8'))
    c_note.url = ctypes.create_string_buffer(note.url.encode('utf-8'))
    return c_note


def copy_notes(notes: list[NoteSchema]) -> CNoteSchemaVec:
    c_notes = (CNoteSchema * len(notes))()
    for i, note in enumerate(notes):
        c_notes[i] = copy_note(note)
    c_notes_vec = CNoteSchemaVec(notes=c_notes, len=len(notes))
    return c_notes_vec


def parse_cnet(input: CNetSchema) -> NetSchema:
    nodes_p = input.nodes
    links_p = input.links
    nodes = [parse_cnet_node(nodes_p[i].contents) for i in range(input.n_len)]
    links = [parse_cnet_link(links_p[i].contents) for i in range(input.l_len)]
    return NetSchema(nodes=nodes, links=links)


def parse_cnet_node(input: CNetNodeSchema) -> NetNodeSchema:
    return NetNodeSchema(
        id=input.id,
        data=input.data.decode(),
        is_md=True if input.is_md == 1 else False,
        pos=Vector(x=input.pos_x, y=input.pos_y)
    )


def parse_cnet_link(input: CNetLinkSchema) -> NetLinkSchema:
    return NetLinkSchema(
        source=input.source,
        target=input.target
    )


net_generator = NetGenerator()
