import random

from ..table import TableHandler
from .rules import RuleSet


class Sampler:
    def __init__(self, table_handler: TableHandler):
        self.table_handler = table_handler

    def sample_by_author(self, author_id: str, n_samples: int, rules: RuleSet) -> list[int]:
        if author_id not in self.table_handler.tweet_meta_table.company_authors:
            raise ValueError(f"Author ID {author_id} not found in tweet meta table.")

        dialog_ids = self.table_handler.retrieve_dialog_ids_by_author_id(author_id)

        dialog_ids_to_use = []
        for dialog_id in dialog_ids:
            dialog = self.table_handler.extract_dialog_contents(dialog_id)

            if rules.apply_all(dialog):
                dialog_ids_to_use.append(dialog_id)

        if len(dialog_ids_to_use) < n_samples:
            print(
                f"Not enough dialog IDs to sample. Found {len(dialog_ids_to_use)}, "
                f"but requested {n_samples}. Returning all available dialog IDs."
            )
            return dialog_ids_to_use

        return random.sample(dialog_ids_to_use, n_samples)
