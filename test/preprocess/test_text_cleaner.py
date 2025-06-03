import pytest

from src.preprocess.cleaner import TextCleaner
from src.preprocess.regex_patterns import RegexPatterns


@pytest.fixture
def regex_patterns():
    return RegexPatterns()


@pytest.fixture
def text_cleaner(regex_patterns):
    return TextCleaner(regex_patterns)


@pytest.fixture
def sample_texts():
    return {
        "with_urls": "Check out https://example.com and http://test.com for more info.",
        "with_emojis": "This text 📖 has emojis 😊",
        "with_parentheses": "This text has (parentheses)",
        "with_mentions": "@mentions This text has @mentions",
        "with_tags": "#tags This text has #tags",
        "with_page_notation": "1/2 This text has page notation 2/2",
        "with_symbols": "@#$% This text has symbols ^&*()",
        "with_html_tags": "<b>This text has HTML tags</b>",
        "without_anything": "This text has nothing special.",
        "empty": "",
    }


class TestTextCleaner:
    def test_remove_urls_removes_all_urls(self, text_cleaner, sample_texts):
        text_with_urls = sample_texts["with_urls"]
        expected_result = "Check out  and  for more info."

        result = text_cleaner.remove_urls(text_with_urls)

        assert result == expected_result

    def test_remove_urls_handles_no_urls(self, text_cleaner, sample_texts):
        text_without_urls = sample_texts["without_anything"]

        result = text_cleaner.remove_urls(text_without_urls)

        assert result == text_without_urls

    def test_remove_urls_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_urls(empty_text)

        assert result == ""

    def test_remove_emojis_removes_all_emojis(self, text_cleaner, sample_texts):
        text_with_emojis = sample_texts["with_emojis"]
        expected_result = "This text  has emojis "

        result = text_cleaner.remove_emojis(text_with_emojis)

        assert result == expected_result

    def test_remove_emojis_handles_no_emojis(self, text_cleaner, sample_texts):
        text_without_emojis = sample_texts["without_anything"]

        result = text_cleaner.remove_emojis(text_without_emojis)

        assert result == text_without_emojis

    def test_remove_emojis_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_emojis(empty_text)

        assert result == ""

    def test_remove_parentheses_with_text_removes_all_parentheses(self, text_cleaner, sample_texts):
        text_with_parentheses = sample_texts["with_parentheses"]
        expected_result = "This text has "

        result = text_cleaner.remove_parentheses_with_text(text_with_parentheses)

        assert result == expected_result

    def test_remove_parentheses_with_text_handles_no_parentheses(self, text_cleaner, sample_texts):
        text_without_parentheses = sample_texts["without_anything"]

        result = text_cleaner.remove_parentheses_with_text(text_without_parentheses)

        assert result == text_without_parentheses

    def test_remove_parentheses_with_text_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_parentheses_with_text(empty_text)

        assert result == ""

    def test_remove_mentions_removes_all_mentions(self, text_cleaner, sample_texts):
        text_with_mentions = sample_texts["with_mentions"]
        expected_result = " This text has "

        result = text_cleaner.remove_mentions(text_with_mentions)

        assert result == expected_result

    def test_remove_mentions_handles_no_mentions(self, text_cleaner, sample_texts):
        text_without_mentions = sample_texts["without_anything"]

        result = text_cleaner.remove_mentions(text_without_mentions)

        assert result == text_without_mentions

    def test_remove_mentions_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_mentions(empty_text)

        assert result == ""

    def test_remove_tags_removes_all_tags(self, text_cleaner, sample_texts):
        text_with_tags = sample_texts["with_tags"]
        expected_result = " This text has "

        result = text_cleaner.remove_tags(text_with_tags)

        assert result == expected_result

    def test_remove_tags_handles_no_tags(self, text_cleaner, sample_texts):
        text_without_tags = sample_texts["without_anything"]

        result = text_cleaner.remove_tags(text_without_tags)

        assert result == text_without_tags

    def test_remove_tags_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_tags(empty_text)

        assert result == ""

    def test_remove_page_notation_removes_all_page_notation(self, text_cleaner, sample_texts):
        text_with_page_notation = sample_texts["with_page_notation"]
        expected_result = " This text has page notation "

        result = text_cleaner.remove_page_notation(text_with_page_notation)

        assert result == expected_result

    def test_remove_page_notation_handles_no_page_notation(self, text_cleaner, sample_texts):
        text_without_page_notation = sample_texts["without_anything"]

        result = text_cleaner.remove_page_notation(text_without_page_notation)

        assert result == text_without_page_notation

    def test_remove_page_notation_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_page_notation(empty_text)

        assert result == ""

    def test_remove_symbol_removes_all_symbols(self, text_cleaner, sample_texts):
        text_with_symbols = sample_texts["with_symbols"]
        expected_result = " This text has symbols "

        result = text_cleaner.remove_symbol(text_with_symbols)

        assert result == expected_result

    def test_remove_symbol_handles_no_symbols(self, text_cleaner, sample_texts):
        text_without_symbols = sample_texts["without_anything"]

        result = text_cleaner.remove_symbol(text_without_symbols)

        assert result == text_without_symbols

    def test_remove_symbol_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_symbol(empty_text)

        assert result == ""

    def test_remove_html_tags_removes_all_html_tags(self, text_cleaner, sample_texts):
        text_with_html_tags = sample_texts["with_html_tags"]
        expected_result = "This text has HTML tags"

        result = text_cleaner.remove_html_tags(text_with_html_tags)

        assert result == expected_result

    def test_remove_html_tags_handles_no_html_tags(self, text_cleaner, sample_texts):
        text_without_html_tags = sample_texts["without_anything"]

        result = text_cleaner.remove_html_tags(text_without_html_tags)

        assert result == text_without_html_tags

    def test_remove_html_tags_handles_empty_text(self, text_cleaner, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_cleaner.remove_html_tags(empty_text)

        assert result == ""
