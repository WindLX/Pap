from pydantic import BaseModel


class SystemConfigModel(BaseModel):
    host: str
    port: int
    title: str
    log_level: str


class PathConfigModel(BaseModel):
    resource_dir: str
    content_dir: str
    log_path: str
    tag_path: str
