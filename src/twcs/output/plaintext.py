from typing import Optional

from ..table import TableHandler
from .rules import RuleSet


class PlainTextGenerator:
    def __init__(self, table_handler: TableHandler, rules: RuleSet):
        self.table_handler = table_handler
        self.rules = rules

    def generate_plain_texts(self, dialog_id: int) -> Optional[list[str]]:
        dialog = self.table_handler.extract_dialog_contents(dialog_id)

        if not self.rules.apply_all(dialog):
            return None

        return dialog.transform_texts()
