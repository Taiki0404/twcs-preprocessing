from preprocess.cleaner import TextCleaner
from preprocess.normalizer import TextNormalizer


class Preprocessor:
    def __init__(self):
        self.cleaner = TextCleaner()
        self.normalizer = TextNormalizer()
