import html
import re
import unicodedata


class TextNormalizer:
    def html_unescape(self, text: str) -> str:
        return html.unescape(text)

    def unify_spaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text)

    def strip(self, text: str) -> str:
        return text.strip()

    def lower(self, text: str) -> str:
        return text.lower()

    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFKC", text)
