import pandas as pd

from ..dialog import Dialog
from .rules import SequenceLength
from .tables import DialogMetaTable, SequenceTable, TextTable, TweetMetaTable


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
