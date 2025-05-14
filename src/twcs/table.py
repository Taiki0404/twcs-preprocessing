import re
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

    def generate_seq_table(self) -> pd.DataFrame:
        dialog_branches = self.twcs.extract_dialog_branches()

        records = []
        for dialog_id, branch in enumerate(dialog_branches):
            for seq in range(len(branch)):
                utterance_id = branch[seq]

                records.append([utterance_id, seq, dialog_id])

        return pd.DataFrame(records, columns=columns["for_seq_table"])

    def generate_tables_as_csv(self, output_dir: str):
        metadata_table = self.generate_metadata_table()
        text_table = self.generate_text_table()
        seq_table = self.generate_seq_table()

        metadata_table.to_csv(f"{output_dir}/metadata.csv", index=False)
        text_table.to_csv(f"{output_dir}/text.csv", index=False)
        seq_table.to_csv(f"{output_dir}/seq.csv", index=False)


class MetadataTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

        self.company_authors = self.retrieve_company_authors()

    def retrieve_company_authors(self) -> list[str]:
        all_authors = self.table["author_id"].unique()

        reject_pattern = re.compile(r"[0-9]+")
        company_authors = []
        for author in all_authors:
            if reject_pattern.match(author):
                continue
            company_authors.append(author)

        return company_authors

    def retrieve_author_by_tweet_id(self, tweet_id: int) -> Optional[str]:
        author = self.table.loc[self.table["tweet_id"] == tweet_id, "author_id"].values

        if author.size == 0:
            return None
        return author[0]

    def retrieve_all_tweet_ids_by_author(self, author_id: str) -> list[int]:
        tweet_ids = self.table.loc[self.table["author_id"] == author_id, "tweet_id"].to_list()
        return tweet_ids


class TextTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

    def retrieve_text_by_tweet_id(self, tweet_id: int) -> Optional[str]:
        text = self.table.loc[self.table["tweet_id"] == tweet_id, "processed_text"].values

        if text.size == 0:
            return None
        return text[0]


class SequenceTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

    def retrieve_tweet_ids_of_dialog_sequence(self, dialog_id: int) -> list[int]:
        df_dialog = self.table[self.table["dialog_id"] == dialog_id]
        df_dialog = df_dialog.sort_values(by="sequence")

        return df_dialog["utterance_id"].tolist()


class TableHandler:
    def __init__(
        self, text_table: TextTable, metadata_table: MetadataTable, seq_table: SequenceTable
    ):
        self.text_table = text_table
        self.metadata_table = metadata_table
        self.seq_table = seq_table

    def extract_dialog_contents(self, dialog_id: int) -> Dialog:
        tweet_ids = self.seq_table.retrieve_tweet_ids_of_dialog_sequence(dialog_id)

        authors = []
        texts = []

        for _id in tweet_ids:
            author = self.metadata_table.retrieve_author_by_tweet_id(_id)
            text = self.text_table.retrieve_text_by_tweet_id(_id)

            if author is None or text is None:
                continue

            authors.append(author)
            texts.append(text)

        return Dialog(authors, texts)
