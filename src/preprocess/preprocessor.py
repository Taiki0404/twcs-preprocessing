from preprocess.cleaner import TextCleaner
from preprocess.normalizer import TextNormalizer
from preprocess.replacer import TextReplacer


class Preprocessor:
    def __init__(self):
        self.cleaner = TextCleaner()
        self.replacer = TextReplacer()
        self.normalizer = TextNormalizer()
