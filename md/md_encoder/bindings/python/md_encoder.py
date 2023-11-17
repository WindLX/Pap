import ctypes

lib = ctypes.CDLL('./target/release/libmdencoder.so')


class CProto(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(ctypes.c_uint8)),
                ("len", ctypes.c_uint32)]


class CProtoVec(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(ctypes.POINTER(CProto))),
                ("len", ctypes.c_uint32)]


class CProtoGenerator(ctypes.Structure):
    _fields_ = [("ctx", ctypes.c_void_p)]


init_proto_generator = lib.init_proto_generator
init_proto_generator.argtypes = [ctypes.c_uint32]
init_proto_generator.restype = ctypes.POINTER(CProtoGenerator)

get_threshold = lib.get_threshold
get_threshold.argtypes = [ctypes.POINTER(CProtoGenerator)]
get_threshold.restype = ctypes.c_uint32

set_threshold = lib.set_threshold
set_threshold.argtypes = [ctypes.POINTER(CProtoGenerator), ctypes.c_uint32]

generate_proto = lib.generate_proto
generate_proto.argtypes = [ctypes.POINTER(CProtoGenerator), ctypes.c_char_p]
generate_proto.restype = ctypes.POINTER(CProtoVec)

free_proto = lib.free_proto
free_proto.argtypes = [ctypes.POINTER(CProto)]

free_proto_vec = lib.free_proto_vec
free_proto_vec.argtypes = [ctypes.POINTER(CProtoVec)]


class MDParser:
    def __init__(self, parallel_threshold: int):
        self.generator = init_proto_generator(parallel_threshold)

    @property
    def parallel_threshold(self) -> int:
        return get_threshold(self.generator)

    @parallel_threshold.setter
    def parallel_threshold(self, value: int):
        set_threshold(self.generator, value)

    def generate(self, input_str: str):
        input_bytes = input_str.encode('utf-8')
        proto_vec = generate_proto(self.generator, input_bytes)
        l = [ctypes.string_at(proto_vec.contents.data[i].contents.data,
                              proto_vec.contents.data[i].contents.len) for i in range(proto_vec.contents.len)]
        free_proto_vec(proto_vec)
        return l

    def __del__(self):
        pass


if __name__ == "__main__":
    g = init_proto_generator(1000)
    set_threshold(g, 1000)

    input_str = "# This is title\n## This is title2"

    md_parser = MDParser(1000)
    l = md_parser.generate(input_str)
    print(l)
