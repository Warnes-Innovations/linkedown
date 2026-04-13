"""Tests for Markdown → LinkedIn conversion."""

from linkedown import md_to_linkedin
from linkedown.unicode_maps import strip_styling, char_style


def test_bold_span():
    result = md_to_linkedin("This is **bold** text.")
    # "bold" should be in bold Unicode
    words = result.split()
    bold_word = next(w for w in words if strip_styling(w) == "bold")
    assert all(char_style(c) == "bold" for c in bold_word if c.isalpha())


def test_italic_span():
    result = md_to_linkedin("This is *italic* text.")
    words = result.split()
    italic_word = next(w for w in words if strip_styling(w) == "italic")
    assert all(char_style(c) == "italic" for c in italic_word if c.isalpha())


def test_code_span():
    result = md_to_linkedin("Run `uvx` now.")
    words = result.split()
    mono_word = next(w for w in words if strip_styling(w) == "uvx")
    assert all(char_style(c) == "monospace" for c in mono_word if c.isalpha())


def test_heading_becomes_bold():
    result = md_to_linkedin("# My Heading\n\nBody text.")
    first_line = result.splitlines()[0]
    assert strip_styling(first_line) == "My Heading"
    assert all(char_style(c) == "bold" for c in first_line if c.isalpha())


def test_bullet_list():
    result = md_to_linkedin("- item one\n- item two\n")
    assert "• item one" in result
    assert "• item two" in result


def test_blockquote():
    result = md_to_linkedin("> quoted text\n")
    assert "│" in result
    assert "quoted text" in result


def test_code_block():
    result = md_to_linkedin("```\nprint('hello')\n```\n")
    assert "▸" in result
    assert "print('hello')" in result


def test_link_expansion():
    result = md_to_linkedin("[GitHub](https://github.com)")
    assert "GitHub" in result
    assert "https://github.com" in result


def test_no_extra_blank_lines():
    md = "Para one.\n\n\n\nPara two.\n"
    result = md_to_linkedin(md)
    assert "\n\n\n" not in result


def test_plain_text_unchanged():
    result = md_to_linkedin("No special formatting here.\n")
    assert result.strip() == "No special formatting here."
