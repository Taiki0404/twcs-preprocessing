import pandas as pd


class SequenceTable:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.table = pd.read_csv(csv_path)

    def retrieve_tweet_ids_of_dialog_sequence(self, dialog_id: int) -> list[int]:
        df_dialog = self.table[self.table["dialog_id"] == dialog_id]
        df_dialog = df_dialog.sort_values(by="sequence")

        return df_dialog["utterance_id"].tolist()
