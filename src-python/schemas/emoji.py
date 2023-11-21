from pydantic import BaseModel


class EmojiSchema(BaseModel):
    unicode: str
    name: str
