import pandas as pd

from .config import columns
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
            for i in range(len(branch) - 1):
                utterance = branch[i]
                response = branch[i + 1]

                records.append([utterance, response, dialog_id])

        return pd.DataFrame(records, columns=columns["for_pair_table"])
