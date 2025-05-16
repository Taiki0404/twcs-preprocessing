import re
from typing import Optional

import pandas as pd

from .config import columns
from .dialog import Dialog
from .rules import SequenceLength
from .twcs import TWCS


class TableGenerator:
    tweet_meta_file = "tweet_meta.csv"
    dialog_meta_file = "dialog_meta.csv"
    text_file = "text.csv"
    seq_file = "seq.csv"

    def __init__(self, twcs: TWCS):
        self.twcs = twcs

    def generate_tweet_meta_table(self) -> pd.DataFrame:
        return self.twcs.retrieve_tweet_meta()

    def generate_dialog_meta_table(
        self, seq_table: pd.DataFrame, tweet_meta_table: pd.DataFrame
    ) -> pd.DataFrame:
        df_merged = seq_table[["dialog_id", "utterance_id"]].merge(
            tweet_meta_table[["tweet_id", "author_id"]],
            left_on="utterance_id",
            right_on="tweet_id",
            how="left",
        )

        dialog_lengths = (
            df_merged.groupby("dialog_id")["utterance_id"].count().reset_index(name="lengths")
        )

        # for文を使わずに、dialog_idごとにauthor_idをリスト化するための書き方
        df_grouped = df_merged.groupby("dialog_id")["author_id"].unique().reset_index()
        supporter_pattern = re.compile(r"[^0-9]+")

        def find_supporter(authors):
            supporters = [
                ath for ath in authors if isinstance(ath, str) and supporter_pattern.match(ath)
            ]
            return supporters[0] if len(supporters) == 1 else None

        df_grouped["supporter"] = df_grouped["author_id"].apply(find_supporter)
        df_grouped["n_authors"] = df_grouped["author_id"].apply(len)
        df_grouped = df_grouped.merge(dialog_lengths, on="dialog_id", how="left")
        df_grouped.drop(columns=["author_id"], inplace=True)

        df_grouped.columns = columns["for_dialog_meta_table"]

        return df_grouped

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

    def generate_tweet_meta_table_as_csv(self, output_dir: str) -> pd.DataFrame:
        path = f"{output_dir}/{self.tweet_meta_file}"

        tweet_meta_table = self.generate_tweet_meta_table()
        tweet_meta_table.to_csv(path, index=False)

        return tweet_meta_table

    def generate_text_table_as_csv(self, output_dir: str) -> pd.DataFrame:
        path = f"{output_dir}/{self.text_file}"

        text_table = self.generate_text_table()
        text_table.to_csv(path, index=False)

        return text_table

    def generate_seq_table_as_csv(self, output_dir: str) -> pd.DataFrame:
        path = f"{output_dir}/{self.seq_file}"

        seq_table = self.generate_seq_table()
        seq_table.to_csv(path, index=False)

        return seq_table

    def generate_dialog_meta_table_as_csv(
        self, output_dir: str, seq_table: pd.DataFrame, tweet_meta_table: pd.DataFrame
    ) -> pd.DataFrame:
        path = f"{output_dir}/{self.dialog_meta_file}"

        dialog_meta_table = self.generate_dialog_meta_table(seq_table, tweet_meta_table)
        dialog_meta_table.to_csv(path, index=False)

        return dialog_meta_table

    def generate_tables_as_csv(self, output_dir: str):
        self.generate_text_table_as_csv(output_dir)
        tweet_meta = self.generate_tweet_meta_table_as_csv(output_dir)
        seq = self.generate_seq_table_as_csv(output_dir)
        self.generate_dialog_meta_table_as_csv(output_dir, seq, tweet_meta)


class TweetMetaTable:
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

    def include_company_authors(self, author_id: str) -> bool:
        return author_id in self.company_authors


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


class TextTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

    def retrieve_text_by_tweet_id(self, tweet_id: int) -> Optional[str]:
        text = self.table.loc[self.table["tweet_id"] == tweet_id, "processed_text"].values[0]

        if not isinstance(text, str):
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
    def __init__(self, tweet_meta_path: str, dialog_meta_path, text_path: str, seq_path: str):
        self.tweet_meta_table = TweetMetaTable(tweet_meta_path)
        self.dialog_meta_table = DialogMetaTable(dialog_meta_path)
        self.text_table = TextTable(text_path)
        self.seq_table = SequenceTable(seq_path)

    def extract_dialog_contents(self, dialog_id: int) -> Dialog:
        tweet_ids = self.seq_table.retrieve_tweet_ids_of_dialog_sequence(dialog_id)

        df = pd.DataFrame({"tweet_id": tweet_ids})

        df = df.merge(
            self.tweet_meta_table.table[["tweet_id", "author_id"]], on="tweet_id", how="left"
        )
        df = df.merge(
            self.text_table.table[["tweet_id", "processed_text"]], on="tweet_id", how="left"
        )

        df = df.dropna(subset=["author_id", "processed_text"])
        authors_seq = df["author_id"].tolist()
        texts_seq = df["processed_text"].tolist()

        return Dialog(authors_seq, texts_seq)

    def retrieve_dialog_ids_by_author_id_with_rules(
        self,
        author_id: str,
        n_authors: int,
        seq_len: SequenceLength,
    ) -> list[int]:
        return self.dialog_meta_table.retrieve_dialog_ids_by_author_with_rules(
            author_id=author_id, n_authors=n_authors, seq_len=seq_len
        )

    def include_company_authors(self, author_id: str) -> bool:
        return self.tweet_meta_table.include_company_authors(author_id)
