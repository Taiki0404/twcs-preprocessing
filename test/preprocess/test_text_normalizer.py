import pytest

from src.preprocess.normalizer import TextNormalizer


@pytest.fixture
def text_normalizer():
    return TextNormalizer()


@pytest.fixture
def sample_texts():
    return {
        "with_html": "This is a &lt;b&gt;bold&lt;/b&gt; text.",
        "with_spaces": "  This   text   has   extra   spaces.  ",
        "with_uppercase": "This text is UPPERCASE.",
        "with_unicode": "This text has\u0020unicode ①②③.",
        "without_anything": "this text has nothing special.",
        "empty": "",
    }


class TestTextNormalizer:
    def test_html_unescape(self, text_normalizer, sample_texts):
        text_with_html = sample_texts["with_html"]
        expected_result = "This is a <b>bold</b> text."

        result = text_normalizer.html_unescape(text_with_html)

        assert result == expected_result

    def test_html_unescape_handles_no_html(self, text_normalizer, sample_texts):
        text_without_html = sample_texts["without_anything"]

        result = text_normalizer.html_unescape(text_without_html)

        assert result == text_without_html

    def test_html_unescape_handles_empty_text(self, text_normalizer, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_normalizer.html_unescape(empty_text)

        assert result == ""

    def test_unify_spaces(self, text_normalizer, sample_texts):
        text_with_spaces = sample_texts["with_spaces"]
        expected_result = " This text has extra spaces. "

        result = text_normalizer.unify_spaces(text_with_spaces)

        assert result == expected_result

    def test_unify_spaces_handles_no_extra_spaces(self, text_normalizer, sample_texts):
        text_without_extra_spaces = sample_texts["without_anything"]

        result = text_normalizer.unify_spaces(text_without_extra_spaces)

        assert result == text_without_extra_spaces

    def test_unify_spaces_handles_empty_text(self, text_normalizer, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_normalizer.unify_spaces(empty_text)

        assert result == ""

    def test_strip(self, text_normalizer, sample_texts):
        text_with_spaces = sample_texts["with_spaces"]
        expected_result = "This   text   has   extra   spaces."

        result = text_normalizer.strip(text_with_spaces)

        assert result == expected_result

    def test_strip_handles_no_extra_spaces(self, text_normalizer, sample_texts):
        text_without_extra_spaces = sample_texts["without_anything"]

        result = text_normalizer.strip(text_without_extra_spaces)

        assert result == text_without_extra_spaces

    def test_strip_handles_empty_text(self, text_normalizer, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_normalizer.strip(empty_text)

        assert result == ""

    def test_lower(self, text_normalizer, sample_texts):
        text_with_uppercase = sample_texts["with_uppercase"]
        expected_result = "this text is uppercase."

        result = text_normalizer.lower(text_with_uppercase)

        assert result == expected_result

    def test_lower_handles_no_uppercase(self, text_normalizer, sample_texts):
        text_without_uppercase = sample_texts["without_anything"]

        result = text_normalizer.lower(text_without_uppercase)

        assert result == text_without_uppercase

    def test_lower_handles_empty_text(self, text_normalizer, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_normalizer.lower(empty_text)

        assert result == ""

    def test_normalize_unicode(self, text_normalizer, sample_texts):
        text_with_unicode = sample_texts["with_unicode"]
        expected_result = "This text has unicode 123."

        result = text_normalizer.normalize_unicode(text_with_unicode)

        assert result == expected_result

    def test_normalize_unicode_handles_no_unicode(self, text_normalizer, sample_texts):
        text_without_unicode = sample_texts["without_anything"]

        result = text_normalizer.normalize_unicode(text_without_unicode)

        assert result == text_without_unicode

    def test_normalize_unicode_handles_empty_text(self, text_normalizer, sample_texts):
        empty_text = sample_texts["empty"]

        result = text_normalizer.normalize_unicode(empty_text)

        assert result == ""
