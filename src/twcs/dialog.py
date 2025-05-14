class Dialog:
    def __init__(self, authors: list[str], texts: list[str]):
        self.authors = authors
        self.texts = texts

    def join_continuous_texts_by_same_author(self) -> list[str]:
        joined_texts = []
        current_author = self.authors[0]
        current_text = self.texts[0]

        for i in range(1, len(self.authors)):
            if self.authors[i] == current_author:
                current_text += " " + self.texts[i]
            else:
                joined_texts.append(current_text)
                current_author = self.authors[i]
                current_text = self.texts[i]

        joined_texts.append(current_text)

        return joined_texts
