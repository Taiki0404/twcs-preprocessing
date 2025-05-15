class Dialog:
    # TODO: add supporter
    def __init__(
        self, authors_seq: list[str], texts_seq: list[str], supporter: str | None, n_authors: int
    ):
        self.authors_seq = authors_seq
        self.texts_seq = texts_seq
        self.supporter = supporter
        self.n_authors = n_authors

    def join_continuous_texts_by_same_author(self) -> list[str]:
        joined_texts = []
        current_author = self.authors_seq[0]
        current_text = self.texts_seq[0]

        for i in range(1, len(self.authors_seq)):
            if self.authors_seq[i] == current_author:
                current_text += " " + self.texts_seq[i]
            else:
                joined_texts.append(current_text)
                current_author = self.authors_seq[i]
                current_text = self.texts_seq[i]

        joined_texts.append(current_text)

        return joined_texts
