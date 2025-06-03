import re

import pandas as pd

from ..twcs import TWCS
from .config import columns


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
