from pydantic import BaseModel


class BasicConfigSchema(BaseModel):
    title: str
    log_level: str


class PathConfigSchema(BaseModel):
    content_dir: str
    log_path: str
    tag_path: str
