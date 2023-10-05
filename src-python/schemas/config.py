from pydantic import BaseModel


class BasicConfigModel(BaseModel):
    title: str
    log_level: str


class PathConfigModel(BaseModel):
    resource_dir: str
    content_dir: str
    log_path: str
    tag_path: str
