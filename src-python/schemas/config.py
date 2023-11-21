from pydantic import BaseModel


class BaseConfigSchema(BaseModel):
    """for impl
    """
    pass


class SystemConfigSchema(BaseConfigSchema):
    host: str
    port: int


class BasicConfigSchema(BaseConfigSchema):
    title: str
    log_level: str


class PathConfigSchema(BaseConfigSchema):
    resource_dir: str
    content_dir: str
    note_dir: str
    log_path: str
    tag_path: str
    emoji_path: str
