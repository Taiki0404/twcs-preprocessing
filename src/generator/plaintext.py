from typing import Optional

import pandas as pd

from .dialog import Dialog
from .rules import RuleSet


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


class PlainTextGenerator:
    def __init__(self, table_handler: TableHandler, rules: RuleSet):
        self.table_handler = table_handler
        self.rules = rules

    def generate_plain_texts(self, dialog_id: int) -> Optional[list[str]]:
        dialog = self.table_handler.extract_dialog_contents(dialog_id)

        if not self.rules.apply_all(dialog):
            return None

        return dialog.transform_texts()
