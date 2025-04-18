from pathlib import Path

import pandas as pd

from .config import columns
from .extractor import TwcsExtractor


class TWCS:
    def __init__(self, twcs_path: str, columns: dict = columns):
        if not Path(twcs_path).exists():
            raise FileNotFoundError(f"TWCS file not found: {twcs_path}")

        self.twcs = pd.read_csv(twcs_path)
        self.columns = columns

        self.extractor = TwcsExtractor()

    def retrieve_metadata(self) -> pd.DataFrame:
        return self.twcs[self.columns["for_meta_table"]]

    def retrieve_text(self) -> pd.DataFrame:
        return self.twcs[self.columns["to_use_in_text_table"]]

    def extract_processed_text(self) -> pd.DataFrame:
        ...
        return

    def extract_dialog_branches(self) -> list[list[int]]:
        dialog_roots = self.twcs[
            pd.isnull(self.twcs["in_response_to_tweet_id"]) & self.twcs["inbound"]
        ]
        dialog_start_ids = dialog_roots["tweet_id"].tolist()

        dialog_branches = self.extractor.extract_all_dialog_branching(
            dialog_start_ids, self.to_dict()
        )

        return dialog_branches

    def to_dict(self) -> dict[int, dict]:
        return self.twcs.set_index("tweet_id").to_dict("index")
