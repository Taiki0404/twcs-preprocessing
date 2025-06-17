from .cleaner import TextCleaner
from .normalizer import TextNormalizer
from .regex_patterns import RegexPatterns


class TextPreprocessingPipeline:
    def __init__(self, regex_patterns: RegexPatterns = RegexPatterns()):
        self.cleaner = TextCleaner(regex_patterns)
        self.normalizer = TextNormalizer()

    def preprocess(self, text: str) -> str:
        if text is None:
            return None
        if not text:
            return text

        steps = [
            self.normalizer.html_unescape,
            self.cleaner.remove_html_tags,
            self.cleaner.remove_emojis,
            # self.cleaner.remove_urls,
            self.cleaner.mask_url,
            self.cleaner.remove_mentions,
            self.cleaner.remove_tags,
            self.cleaner.remove_parentheses_with_text,
            self.cleaner.remove_page_notation,
            self.cleaner.remove_symbol,
            self.normalizer.unify_spaces,
            self.normalizer.strip,
            self.normalizer.lower,
            self.normalizer.normalize_unicode,
        ]

        for step in steps:
            text = step(text)

            if not text:
                return text

        return text
