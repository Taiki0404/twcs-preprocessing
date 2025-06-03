import re
from typing import Optional

import pandas as pd


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
