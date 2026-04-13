"""Tests for unicode_maps — forward and inverse character conversions."""

from linkedown.unicode_maps import (
    char_style,
    strip_styling,
    to_bold,
    to_italic,
    to_monospace,
    to_bold_italic,
)


def test_to_bold_letters():
    result = to_bold("Hello")
    assert result != "Hello"
    assert strip_styling(result) == "Hello"
    assert all(char_style(c) == "bold" for c in result if c.isalpha() or c.isdigit())


def test_to_bold_digits():
    result = to_bold("123")
    assert strip_styling(result) == "123"


def test_to_bold_preserves_punctuation():
    result = to_bold("Hello, World!")
    assert "," in result
    assert "!" in result
    assert " " in result


def test_to_italic_letters():
    result = to_italic("hello")
    assert result != "hello"
    assert strip_styling(result) == "hello"


def test_to_italic_preserves_digits():
    result = to_italic("abc123")
    assert result.endswith("123")  # digits unchanged


def test_to_monospace_letters_and_digits():
    result = to_monospace("code42")
    assert strip_styling(result) == "code42"
    assert all(char_style(c) == "monospace" for c in result if c.isalpha() or c.isdigit())


def test_to_bold_italic():
    result = to_bold_italic("Hi")
    assert strip_styling(result) == "Hi"


def test_strip_styling_plain_text():
    assert strip_styling("plain text") == "plain text"


def test_strip_styling_mixed():
    bold = to_bold("BOLD")
    italic = to_italic("italic")
    assert strip_styling(bold + " " + italic) == "BOLD italic"


def test_char_style_plain_returns_none():
    assert char_style("A") is None
    assert char_style(" ") is None
    assert char_style("!") is None


def test_char_style_bold():
    bold_a = to_bold("A")
    assert char_style(bold_a) == "bold"


def test_char_style_italic():
    italic_a = to_italic("A")
    assert char_style(italic_a) == "italic"


def test_char_style_monospace():
    mono_a = to_monospace("a")
    assert char_style(mono_a) == "monospace"
