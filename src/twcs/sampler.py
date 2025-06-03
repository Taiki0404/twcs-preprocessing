import random

from .table.handler import TableHandler
from .table.rules import SequenceLength


class Sampler:
    def __init__(self, table_handler: TableHandler):
        self.table_handler = table_handler

    def sample_dialog_id_by_author(
        self, author_id: str, n_samples: int, n_authors: int, seq_len: SequenceLength
    ) -> list[int]:
        if not self.table_handler.include_company_authors(author_id):
            raise ValueError(f"Author ID {author_id} not found in tweet meta table.")

        dialog_ids = self.table_handler.retrieve_dialog_ids_by_author_id_with_rules(
            author_id=author_id,
            n_authors=n_authors,
            seq_len=seq_len,
        )

        if len(dialog_ids) < n_samples:
            print(
                f"Not enough dialog IDs to sample. Found {len(dialog_ids)}, "
                f"but requested {n_samples}. Returning all available dialog IDs."
            )
            return dialog_ids

        return random.sample(dialog_ids, n_samples)
