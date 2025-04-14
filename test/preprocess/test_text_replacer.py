import pytest

from src.preprocess.cleaner import TextCleaner


class MockRegexPatterns:
    URL = r"https?://(?:www\.)?[^\s/$.?#].[^\s]*"


@pytest.fixture
def text_cleaner():
    return TextCleaner(regex_patterns=MockRegexPatterns)


@pytest.fixture
def sample_texts():
    return {
        "with_urls": "Check out https://example.com and http://test.com for more info.",
        "without_anything": "This text has nothing special",
        "empty": "",
    }


class TestTextReplacer:
    def test_replace_urls_replaces_all_urls(self, text_cleaner, sample_texts):
        text_with_urls = sample_texts["with_urls"]
        expected_result = "Check out [URL] and [URL] for more info."

        result = text_cleaner.replace_urls(text_with_urls, "[URL]")

        assert result == expected_result

    def test_replace_urls_handles_no_urls(self, text_cleaner, sample_texts):
        text_without_urls = sample_texts["without_anything"]

        result = text_cleaner.replace_urls(text_without_urls)

        assert result == text_without_urls

    def test_replace_urls_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.replace_urls(empty_text)

        assert result == ""
