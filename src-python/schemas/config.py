from pydantic import BaseModel


class BasicConfigSchema(BaseModel):
    title: str
    log_level: str


class PathConfigSchema(BaseModel):
    resource_dir: str
    content_dir: str
    log_path: str
    tag_path: str
