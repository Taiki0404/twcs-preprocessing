from pathlib import Path

import pandas as pd

import settings


class TableGenerator:
    def __init__(self, twcs: pd.DataFrame):
        self.twcs = twcs
        self.metadata_table = self.__create_metadata_table()
        self.text_table = self.__create_text_table()
        self.pair_table = self.__create_pair_table()

    def __create_metadata_table(self) -> pd.DataFrame:
        return self.twcs[settings.META_TABLE_COLUMNS]

    def __create_text_table(self) -> pd.DataFrame:
        # TODO: テキストテーブルを生成するロジックを実装する
        return pd.DataFrame()

    def __create_pair_table(self) -> pd.DataFrame:
        # TODO: ペアテーブルを生成するロジックを実装する
        return pd.DataFrame()

    def to_csv(self, dir: str = "output") -> None:
        p_dir = Path(dir)
        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_table.to_csv(f"{dir}/metadata.csv", index=False)
        self.text_table.to_csv(f"{dir}/text.csv", index=False)
        self.pair_table.to_csv(f"{dir}/pair.csv", index=False)


if __name__ == "__main__":
    sample = pd.read_csv("sample.csv")

    generator = TableGenerator(sample)
    generator.to_csv()
