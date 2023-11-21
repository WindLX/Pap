from sqlite3 import connect

from schemas.emoji import EmojiSchema
from service.config import path_config


class EmojiGetter:
    """A emoji unicode getter
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def search(self, emoji: str) -> list[EmojiSchema] | None:
        """
        Search emoji from database.
        """
        conn = connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT unicode, name FROM emoji WHERE name LIKE ?", ('%' + emoji + '%',))
        result = cursor.fetchall()

        conn.close()
        if not result:
            return []

        emoji_list = [EmojiSchema(unicode=row[0], name=row[1])
                      for row in result]
        return emoji_list


emoji_getter = EmojiGetter(path_config.emoji_path)
