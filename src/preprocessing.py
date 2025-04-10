class TextCleaner:
    def remove_emojis(self, text: str) -> str:
        return ""

    def remove_urls(self, text: str) -> str:
        return ""

    def remove_punctuation(self, text: str) -> str:
        return ""

    def remove_punc_in_jp(self, text: str) -> str:
        return ""

    def remove_parentheses(self, text: str) -> str:
        return ""

    def remove_mentions(self, text: str) -> str:
        return ""

    def remove_tags(self, text: str) -> str:
        return ""

    def remove_page_notation(self, text: str) -> str:
        return ""

    def replace_urls(self, text: str) -> str:
        return ""


class TextNormalizer:
    def html_unescape(self, text: str) -> str:
        return ""

    def unify_spaces(self, text: str) -> str:
        return ""

    def strip(self, text: str) -> str:
        return ""

    def lower(self, text: str) -> str:
        return ""

    def replace_end_punctuation(self, text: str) -> str:
        return ""

    def replace_commas(self, text: str) -> str:
        return ""

    def replace_garbling(self, text: str) -> str:
        return ""

    def add_piriod(self, text: str) -> str:
        return ""


class Preprocessor:
    def __init__(self):
        self.cleaner = TextCleaner()
        self.normalizer = TextNormalizer()
