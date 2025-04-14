import re

import emoji

from .regex_patterns import RegexPatterns


class TextCleaner:
    def __init__(self, regex_patterns: RegexPatterns):
        self.regex_patterns = regex_patterns

    def remove_emojis(self, text: str) -> str:
        return emoji.replace_emoji(text, replace="")

    def remove_urls(self, text: str) -> str:
        return re.sub(self.regex_patterns.URL, "", text)

    def remove_parentheses_with_text(self, text: str) -> str:
        return re.sub(self.regex_patterns.PARENTHESES_WITH_TEXT, "", text)

    def remove_mentions(self, text: str) -> str:
        return re.sub(self.regex_patterns.MENTIONS, "", text)

    def remove_tags(self, text: str) -> str:
        return re.sub(self.regex_patterns.TAGS, "", text)

    def remove_page_notation(self, text: str) -> str:
        return re.sub(self.regex_patterns.PAGE_NOTATION, "", text)

    def remove_html_tags(self, text: str) -> str:
        return re.sub(r"<.*?>", "", text)

    def remove_symbol(self, text: str) -> str:
        return re.sub(self.regex_patterns.SYMBOLS, "", text)

    def clean(self, text: str) -> str:
        if not text:
            return text

        steps = [
            self.remove_emojis,
            self.remove_urls,
            self.remove_parentheses_with_text,
            self.remove_mentions,
            self.remove_tags,
            self.remove_page_notation,
            self.remove_html_tags,
            self.remove_symbol,
        ]

        for step in steps:
            text = step(text)

        return text
