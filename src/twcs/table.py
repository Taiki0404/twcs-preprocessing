from typing import Optional

import pandas as pd

from .config import columns
from .dialog import Dialog
from .twcs import TWCS


class TableGenerator:
    def __init__(self, twcs: TWCS):
        self.twcs = twcs

    def generate_metadata_table(self) -> pd.DataFrame:
        return self.twcs.retrieve_metadata()

    def generate_text_table(self) -> pd.DataFrame:
        tweet_ids = self.twcs.extract_tweet_ids()
        processed_texts = self.twcs.extract_processed_text()

        records = zip(tweet_ids, processed_texts)

        return pd.DataFrame(records, columns=columns["for_text_table"])

    def generate_pair_table(self) -> pd.DataFrame:
        dialog_branches = self.twcs.extract_dialog_branches()

        records = []
        for dialog_id, branch in enumerate(dialog_branches):
            for seq in range(len(branch)):
                utterance_id = branch[seq]

                records.append([utterance_id, seq, dialog_id])

        return pd.DataFrame(records, columns=columns["for_pair_table"])

    def generate_tables_as_csv(self, output_dir: str):
        metadata_table = self.generate_metadata_table()
        text_table = self.generate_text_table()
        pair_table = self.generate_pair_table()

        metadata_table.to_csv(f"{output_dir}/metadata.csv", index=False)
        text_table.to_csv(f"{output_dir}/text.csv", index=False)
        pair_table.to_csv(f"{output_dir}/pair.csv", index=False)


class TableHandler:
    def __init__(
        self, text_table: pd.DataFrame, metadata_table: pd.DataFrame, pair_table: pd.DataFrame
    ):
        self.text_table = text_table
        self.metadata_table = metadata_table
        self.pair_table = pair_table

    def retrieve_tweet_ids_of_dialog_sequence(self, dialog_id: int) -> list:
        df_dialog = self.pair_table[self.pair_table["dialog_id"] == dialog_id]
        df_dialog = df_dialog.sort_values(by="sequence")

        return df_dialog["utterance_id"].tolist()

    def retrieve_text_by_tweet_id(self, tweet_id: int) -> Optional[str]:
        text = self.text_table.loc[self.text_table["tweet_id"] == tweet_id, "processed_text"].values

        if text.size == 0:
            return None
        return text[0]

    def retrieve_author_by_tweet_id(self, tweet_id: int) -> Optional[str]:
        author = self.metadata_table.loc[
            self.metadata_table["tweet_id"] == tweet_id, "author_id"
        ].values

        if author.size == 0:
            return None
        return author[0]

    def extract_dialog_contents(self, dialog_id: int) -> Dialog:
        tweet_ids = self.retrieve_tweet_ids_of_dialog_sequence(dialog_id)

        authors = []
        texts = []

        for _id in tweet_ids:
            author = self.retrieve_author_by_tweet_id(_id)
            text = self.retrieve_text_by_tweet_id(_id)

            if author is None or text is None:
                continue

            authors.append(author)
            texts.append(text)

        return Dialog(authors, texts)
