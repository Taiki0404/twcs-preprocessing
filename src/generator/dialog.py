class TextTransformer:
    def __init__(self): ...

    @staticmethod
    def join_continuous_texts_by_same_author(authors: list[str], texts: list[str]) -> list:
        joined_texts = []
        current_author = authors[0]
        current_text = texts[0]

        for i in range(1, len(authors)):
            if authors[i] == current_author:
                current_text += " " + texts[i]
            else:
                joined_texts.append(current_text)
                current_author = authors[i]
                current_text = texts[i]

        joined_texts.append(current_text)

        return joined_texts


class Dialog:
    def __init__(self, authors: list[str], texts: list[str]):
        self.authors = authors
        self.texts = texts

        self.text_transformer = TextTransformer()

    def transform_texts(self) -> list:
        return self.text_transformer.join_continuous_texts_by_same_author(self.authors, self.texts)
