from pathlib import Path

import pandas as pd

from .config import columns


class TWCS:
    def __init__(self, twcs_path: str, columns: dict = columns):
        if not Path(twcs_path).exists():
            raise FileNotFoundError(f"TWCS file not found: {twcs_path}")

        self.twcs = pd.read_csv(twcs_path)
        self.columns = columns

    def retrieve_metadata(self) -> pd.DataFrame:
        return self.twcs[self.columns["for_meta_table"]]

    def retrieve_text(self) -> pd.DataFrame:
        return self.twcs[self.columns["to_use_in_text_table"]]

    def extract_processed_text(self) -> pd.DataFrame:
        ...
        return

    def extract_dialog_pairs(self) -> pd.DataFrame:
        ...
        return
