from typing import Optional

from ..table import TableHandler


class PlainTextGenerator:
    def __init__(self, table_handler: TableHandler):
        self.table_handler = table_handler

    def generate_plain_texts(self, dialog_id: int) -> Optional[list[str]]:
        dialog = self.table_handler.extract_dialog_contents(dialog_id)

        return dialog.join_continuous_texts_by_same_author()
