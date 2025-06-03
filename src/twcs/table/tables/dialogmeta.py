from typing import Optional

import pandas as pd

from ..rules import SequenceLength


class DialogMetaTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

    def retrieve_supporter_by_dialog_id(self, dialog_id: int) -> Optional[str]:
        supporter = self.table.loc[self.table["dialog_id"] == dialog_id, "supporter"].values[0]

        if not isinstance(supporter, str):
            return None
        return supporter

    def retrieve_n_authors_by_dialog_id(self, dialog_id: int) -> int:
        return self.table.loc[self.table["dialog_id"] == dialog_id, "n_authors"].values[0]

    def retrieve_dialog_ids_by_author_with_rules(
        self, author_id: str, n_authors: int, seq_len: SequenceLength
    ) -> list[int]:
        df = self.table[
            (self.table["supporter"] == author_id)
            & (self.table["n_authors"] == n_authors)
            & (self.table["length"].between(seq_len.min, seq_len.max))
        ]

        return df["dialog_id"].tolist()
