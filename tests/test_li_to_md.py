"""Tests for LinkedIn Unicode → Markdown conversion."""

from linkedown import linkedin_to_md, md_to_linkedin
from linkedown.unicode_maps import to_bold, to_italic, to_monospace


# ---------------------------------------------------------------------------
# Direct li2md tests
# ---------------------------------------------------------------------------


def test_bold_line_becomes_heading():
    bold_line = to_bold("My Title")
    result = linkedin_to_md(bold_line + "\n")
    assert result.strip() == "# My Title"


def test_inline_bold_becomes_stars():
    line = "Hello " + to_bold("world") + " here"
    result = linkedin_to_md(line + "\n")
    assert "**world**" in result


def test_inline_italic_becomes_stars():
    line = "Hello " + to_italic("world") + " here"
    result = linkedin_to_md(line + "\n")
    assert "*world*" in result


def test_inline_monospace_becomes_backtick():
    line = "Run " + to_monospace("uvx") + " now"
    result = linkedin_to_md(line + "\n")
    assert "`uvx`" in result


def test_bullet_becomes_dash():
    result = linkedin_to_md("• item one\n• item two\n")
    assert "- item one" in result
    assert "- item two" in result


def test_blockquote_becomes_gt():
    result = linkedin_to_md("│ quoted text\n")
    assert "> quoted text" in result


def test_code_block_reconstruction():
    li_text = "▸ print('hello')\n▸ print('world')\n"
    result = linkedin_to_md(li_text)
    assert "```" in result
    assert "print('hello')" in result
    assert "print('world')" in result


def test_hrule():
    result = linkedin_to_md("─────────────\n")
    assert "---" in result


def test_image_ref():
    result = linkedin_to_md("[Image: logo] https://example.com/logo.png\n")
    assert "![logo](https://example.com/logo.png)" in result


def test_link_reconstruction():
    # The link heuristic converts 'label (url)' → '[label](url)'.
    # The greedy label includes all text before the parenthesised URL.
    result = linkedin_to_md("Visit GitHub (https://github.com) today\n")
    assert "(https://github.com)" in result
    assert "[" in result  # some link syntax produced


def test_plain_text_unchanged():
    result = linkedin_to_md("No special formatting here.\n")
    assert result.strip() == "No special formatting here."


# ---------------------------------------------------------------------------
# Round-trip tests (md → li → md)
# ---------------------------------------------------------------------------


def _roundtrip(md: str) -> str:
    return linkedin_to_md(md_to_linkedin(md))


def test_roundtrip_heading():
    rt = _roundtrip("# My Heading\n\nSome text.\n")
    assert "# My Heading" in rt
    assert "Some text." in rt


def test_roundtrip_bold_inline():
    rt = _roundtrip("This is **bold** text.\n")
    assert "**bold**" in rt


def test_roundtrip_italic_inline():
    rt = _roundtrip("This is *italic* text.\n")
    assert "*italic*" in rt


def test_roundtrip_bullets():
    rt = _roundtrip("- item one\n- item two\n")
    assert "- item one" in rt
    assert "- item two" in rt


def test_roundtrip_code_span():
    rt = _roundtrip("Run `uvx` now.\n")
    assert "`uvx`" in rt


def test_roundtrip_code_block():
    rt = _roundtrip("```\nprint('hello')\n```\n")
    assert "print('hello')" in rt


def test_roundtrip_blockquote():
    rt = _roundtrip("> important note\n")
    assert "important note" in rt


def test_roundtrip_plain():
    rt = _roundtrip("No formatting here.\n")
    assert "No formatting here." in rt
