import re

from .regex_patterns import RegexPatterns


class TextReplacer:
    def __init__(self):
        self.regex_patterns = RegexPatterns()

    def replace_urls(self, text: str, replacement: str = "") -> str:
        return re.sub(self.regex_patterns.URL, replacement, text)
