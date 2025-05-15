import re
from typing import Optional

import pandas as pd

from .config import columns
from .dialog import Dialog
from .twcs import TWCS


class TableGenerator:
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
        tweet_meta_table = self.generate_tweet_meta_table()
        tweet_meta_table.to_csv(f"{output_dir}/tweet_meta.csv", index=False)

        return tweet_meta_table

    def generate_text_table_as_csv(self, output_dir: str) -> pd.DataFrame:
        text_table = self.generate_text_table()
        text_table.to_csv(f"{output_dir}/text.csv", index=False)

        return text_table

    def generate_seq_table_as_csv(self, output_dir: str) -> pd.DataFrame:
        seq_table = self.generate_seq_table()
        seq_table.to_csv(f"{output_dir}/seq.csv", index=False)

        return seq_table

    def generate_dialog_meta_table_as_csv(
        self, output_dir: str, seq_table: pd.DataFrame, tweet_meta_table: pd.DataFrame
    ) -> pd.DataFrame:
        dialog_meta_table = self.generate_dialog_meta_table(seq_table, tweet_meta_table)
        dialog_meta_table.to_csv(f"{output_dir}/dialog_meta.csv", index=False)

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

    def retrieve_all_tweet_ids_by_author(self, author_id: str) -> list[int]:
        tweet_ids = self.table.loc[self.table["author_id"] == author_id, "tweet_id"].to_list()
        return tweet_ids


class DialogMetaTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

    def retrieve_supporter_by_dialog_id(self, dialog_id: int) -> Optional[str]:
        supporter = self.table.loc[self.table["dialog_id"] == dialog_id, "supporter"].values[0]

        if not isinstance(supporter, str):
            return None
        return supporter


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

    def retrieve_dialog_ids_by_tweet_id(self, tweet_id: int) -> list[int]:
        return self.table.loc[self.table["utterance_id"] == tweet_id, "dialog_id"].to_list()

    def retrieve_dialog_ids_by_tweet_ids(self, tweet_ids: list[int]) -> list[int]:
        dialog_ids = []
        for tweet_id in tweet_ids:
            dialog_ids.extend(self.retrieve_dialog_ids_by_tweet_id(tweet_id))

        return list(set(dialog_ids))


class TableHandler:
    def __init__(self, text_path: str, tweet_meta_path: str, seq_path: str):
        self.text_table = TextTable(text_path)
        self.tweet_meta_table = TweetMetaTable(tweet_meta_path)
        # TODO: 対話メタテーブルの読み込み
        # self.dialog_meta_table = DialogMetaTable(dialog_meta_path)
        self.seq_table = SequenceTable(seq_path)

    def extract_dialog_contents(self, dialog_id: int) -> Dialog:
        tweet_ids = self.seq_table.retrieve_tweet_ids_of_dialog_sequence(dialog_id)
        # TODO: 対話メタテーブルからサポーターを取得
        # supporter = self.dialog_meta_table.retrieve_supporter_by_dialog_id(dialog_id)

        authors = []
        texts = []

        for _id in tweet_ids:
            author = self.tweet_meta_table.retrieve_author_by_tweet_id(_id)
            text = self.text_table.retrieve_text_by_tweet_id(_id)

            if author is None or text is None:
                continue

            authors.append(author)
            texts.append(text)

        # TODO: サポーターをDialogに追加
        return Dialog(authors, texts)  # , supporter)

    def retrieve_all_tweet_ids_by_author(self, author_id: str) -> list[int]:
        return self.tweet_meta_table.retrieve_all_tweet_ids_by_author(author_id)

    def retrieve_dialog_ids_by_tweet_ids(self, tweet_ids: list[int]) -> list[int]:
        return self.seq_table.retrieve_dialog_ids_by_tweet_ids(tweet_ids)
