import ctypes
from schemas.note import NoteSchema
from schemas.net import NetSchema, NetNodeSchema, NetLinkSchema

lib = ctypes.CDLL('./md_net.dll')


class CNoteSchema(ctypes.Structure):
    _fields_ = [("id", ctypes.c_uint32),
                ("name", ctypes.POINTER(ctypes.c_char)),
                ("url", ctypes.POINTER(ctypes.c_char)),
                ("len", ctypes.c_uint32)]


class CNoteSchemaVec(ctypes.Structure):
    _fields_ = [("notes", ctypes.POINTER(CNoteSchema)),
                ("len", ctypes.c_uint32)]


class CNetNodeSchema(ctypes.Structure):
    _fields_ = [("id", ctypes.c_uint32),
                ("dat", ctypes.POINTER(ctypes.c_char)),
                ("is_md", ctypes.c_uint32),
                ("pos_x", ctypes.c_uint32),
                ("pos_y", ctypes.c_uint32)]


class CNetLinkSchema(ctypes.Structure):
    _fields_ = [("source", ctypes.c_uint32),
                ("target", ctypes.c_uint32)]


class CNetSchema(ctypes.Structure):
    _fields_ = [("nodes", ctypes.POINTER(CNetNodeSchema)),
                ("links", ctypes.POINTER(CNetLinkSchema)),
                ("n_len", ctypes.c_uint32),
                ("l_len", ctypes.c_uint32)]


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
        free_net_schema(cnet)
        net = parse_cnet(cnet.content)
        return net

    def __del__(self):
        pass


def copy_note(note: NoteSchema) -> CNoteSchema:
    pass


def copy_notes(notes: list[NoteSchema]) -> CNoteSchemaVec:
    pass


def parse_cnet(input: CNetSchema) -> NetSchema:
    pass


def parse_cnet_node(input: CNetNodeSchema) -> NetNodeSchema:
    pass


def parse_cnet_link(input: CNetLinkSchema) -> NetLinkSchema:
    pass


net_generator = NetGenerator()
