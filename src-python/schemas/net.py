from pydantic import BaseModel


class Vector(BaseModel):
    x: int
    y: int


class NetNodeSchema (BaseModel):
    id: int
    data: str
    is_md: bool
    pos: Vector


class NetLinkSchema (BaseModel):
    source: int
    target: int


class NetSchema (BaseModel):
    nodes: list[NetNodeSchema]
    links: list[NetLinkSchema]
