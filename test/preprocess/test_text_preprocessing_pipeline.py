import pytest

from src.preprocess.preprocessing_pipeline import TextPreprocessingPipeline
from src.preprocess.regex_patterns import RegexPatterns


@pytest.fixture
def regex_patterns():
    return RegexPatterns()


@pytest.fixture
def preprocessing_pipeline(regex_patterns):
    return TextPreprocessingPipeline(regex_patterns)


class TestTextPreprocessingPipeline:
    @pytest.mark.parametrize(
        "input_text, expected_output",
        [
            ("Hello <b>world</b>!", "hello world"),
            ("Visit https://example.com", "visit"),
            ("@user Check this out!", "check this out"),
            ("#hashtag is trending", "is trending"),
            ("(Note: confidential)", ""),
            ("This is first page 1/2", "this is first page"),
            ("Symbols like $%^&*", "symbols like"),
            ("   Extra   spaces   ", "extra spaces"),
            ("normalize\u0020unicode ①②③.", "normalize unicode 123"),
            ("", ""),
        ],
    )
    def test_preprocess(self, preprocessing_pipeline, input_text, expected_output):
        assert preprocessing_pipeline.preprocess(input_text) == expected_output

    def test_preprocess_empty_string(self, preprocessing_pipeline):
        assert preprocessing_pipeline.preprocess("") == ""

    def test_preprocess_none(self, preprocessing_pipeline):
        assert preprocessing_pipeline.preprocess(None) is None
