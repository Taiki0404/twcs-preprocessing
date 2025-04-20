from pathlib import Path

import pandas as pd

from ..preprocess.preprocessing_pipeline import TextPreprocessingPipeline
from .config import columns
from .extractor import TwcsDialogExtractor


class TWCS:
    def __init__(self, twcs_path: str, columns_config: dict = columns):
        if not Path(twcs_path).exists():
            raise FileNotFoundError(f"TWCS file not found: {twcs_path}")

        self.twcs = pd.read_csv(twcs_path)
        self.columns_config = columns_config

        self.extractor = TwcsDialogExtractor()
        self.preprocessor = TextPreprocessingPipeline()

    def retrieve_metadata(self) -> pd.DataFrame:
        return self.twcs[self.columns_config["for_meta_table"]]

    def extract_tweet_ids(self) -> list[int]:
        return self.twcs["tweet_id"].tolist()

    def extract_processed_text(self) -> list[str]:
        texts = self.twcs["text"].tolist()

        processed_texts = []
        for text in texts:
            processed_text = self.preprocessor.preprocess(text)
            processed_texts.append(processed_text)

        return processed_texts

    def extract_dialog_branches(self) -> list[list[int]]:
        dialog_roots = self.twcs[
            pd.isnull(self.twcs["in_response_to_tweet_id"]) & self.twcs["inbound"]
        ]
        dialog_start_ids = dialog_roots["tweet_id"].tolist()

        dialog_branches = self.extractor.extract_all_dialog_branching(
            dialog_start_ids, self.to_dict(self.columns_config["to_use_in_pair_table"])
        )

        return dialog_branches

    def to_dict(self, use_col: list = []) -> dict[int, dict]:
        if not use_col:
            return self.twcs.set_index("tweet_id").to_dict("index")

        if "tweet_id" not in use_col:
            raise ValueError("use_col must include 'tweet_id'")

        return self.twcs[use_col].set_index("tweet_id").to_dict("index")
