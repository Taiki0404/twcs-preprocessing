from typing import Optional

import pandas as pd


class TextTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

    def retrieve_text_by_tweet_id(self, tweet_id: int) -> Optional[str]:
        text = self.table.loc[self.table["tweet_id"] == tweet_id, "processed_text"].values[0]

        if not isinstance(text, str):
            return None
        return text[0]
