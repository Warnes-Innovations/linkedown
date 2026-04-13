"""Unicode character mapping tables for LinkedIn ↔ Markdown text style transformations.

The forward (Markdown → LinkedIn) character maps and conversion functions in this
module are derived from md-to-linkedin by Scott Henning
(https://github.com/shenning00/md-to-linkedin), licensed MIT.

The inverse (LinkedIn → Markdown) maps and ``from_*`` functions are original additions
contributed back to that project via upstream PR.

Unicode ranges used:
- Bold:        U+1D5D4–U+1D607 (A–Z, a–z),  U+1D7EC–U+1D7F5 (0–9)  [Sans-Serif Bold]
- Italic:      U+1D434–U+1D467 (A–Z, a–z)
- Bold-Italic: U+1D468–U+1D49B (A–Z, a–z)
- Monospace:   U+1D670–U+1D6A3 (A–Z, a–z),  U+1D7F6–U+1D7FF (0–9)

Unsupported characters (punctuation, whitespace, etc.) pass through unchanged in
both directions.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------------
# Forward maps: ASCII → Unicode styled
# ---------------------------------------------------------------------------

# Bold (Mathematical Sans-Serif Bold)
# A-Z → U+1D5D4-U+1D5ED
BOLD_UPPER: Final[dict[str, str]] = {
    chr(ord("A") + i): chr(0x1D5D4 + i) for i in range(26)
}
# a-z → U+1D5EE-U+1D607
BOLD_LOWER: Final[dict[str, str]] = {
    chr(ord("a") + i): chr(0x1D5EE + i) for i in range(26)
}
# 0-9 → U+1D7EC-U+1D7F5
BOLD_DIGITS: Final[dict[str, str]] = {
    chr(ord("0") + i): chr(0x1D7EC + i) for i in range(10)
}

# Italic (Mathematical Italic)
# A-Z → U+1D434-U+1D44D
# Note: H (capital) is contiguous; h (lowercase) has a gap at U+210E
ITALIC_UPPER: Final[dict[str, str]] = {
    chr(ord("A") + i): chr(0x1D434 + i) for i in range(26)
}
# a-z → U+1D44E-U+1D467  (italic 'h' is special: U+210E)
ITALIC_LOWER: Final[dict[str, str]] = {
    chr(ord("a") + i): chr(0x1D44E + i) if i != 7 else chr(0x210E) for i in range(26)
}

# Sans-Serif Italic (used by some external LinkedIn formatting tools)
# A-Z → U+1D608-U+1D621
_SANS_SERIF_ITALIC_UPPER: Final[dict[str, str]] = {
    chr(ord("A") + i): chr(0x1D608 + i) for i in range(26)
}
# a-z → U+1D622-U+1D63B
_SANS_SERIF_ITALIC_LOWER: Final[dict[str, str]] = {
    chr(ord("a") + i): chr(0x1D622 + i) for i in range(26)
}

# Bold-Italic (Mathematical Bold Italic)
# A-Z → U+1D468-U+1D481
BOLD_ITALIC_UPPER: Final[dict[str, str]] = {
    chr(ord("A") + i): chr(0x1D468 + i) for i in range(26)
}
# a-z → U+1D482-U+1D49B
BOLD_ITALIC_LOWER: Final[dict[str, str]] = {
    chr(ord("a") + i): chr(0x1D482 + i) for i in range(26)
}

# Monospace (Mathematical Monospace)
# A-Z → U+1D670-U+1D689
MONOSPACE_UPPER: Final[dict[str, str]] = {
    chr(ord("A") + i): chr(0x1D670 + i) for i in range(26)
}
# a-z → U+1D68A-U+1D6A3
MONOSPACE_LOWER: Final[dict[str, str]] = {
    chr(ord("a") + i): chr(0x1D68A + i) for i in range(26)
}
# 0-9 → U+1D7F6-U+1D7FF
MONOSPACE_DIGITS: Final[dict[str, str]] = {
    chr(ord("0") + i): chr(0x1D7F6 + i) for i in range(10)
}

# ---------------------------------------------------------------------------
# Inverse maps: Unicode styled → ASCII  (derived automatically)
# ---------------------------------------------------------------------------

_BOLD_TO_ASCII: Final[dict[str, str]] = {
    **{v: k for k, v in BOLD_UPPER.items()},
    **{v: k for k, v in BOLD_LOWER.items()},
    **{v: k for k, v in BOLD_DIGITS.items()},
}
_ITALIC_TO_ASCII: Final[dict[str, str]] = {
    **{v: k for k, v in ITALIC_UPPER.items()},
    **{v: k for k, v in ITALIC_LOWER.items()},
    # sans-serif italic (produced by some external tools) also maps to italic
    **{v: k for k, v in _SANS_SERIF_ITALIC_UPPER.items()},
    **{v: k for k, v in _SANS_SERIF_ITALIC_LOWER.items()},
}
_BOLD_ITALIC_TO_ASCII: Final[dict[str, str]] = {
    **{v: k for k, v in BOLD_ITALIC_UPPER.items()},
    **{v: k for k, v in BOLD_ITALIC_LOWER.items()},
}
_MONOSPACE_TO_ASCII: Final[dict[str, str]] = {
    **{v: k for k, v in MONOSPACE_UPPER.items()},
    **{v: k for k, v in MONOSPACE_LOWER.items()},
    **{v: k for k, v in MONOSPACE_DIGITS.items()},
}

# Combined reverse map: any styled char → (ascii_char, style_name)
# Each source dict is inverted independently to avoid key collisions when merging
# ASCII→Unicode dicts (which share ASCII keys).
_ALL_STYLED_TO_ASCII: Final[dict[str, tuple[str, str]]] = {
    # Bold
    **{v: (k, "bold") for k, v in BOLD_UPPER.items()},
    **{v: (k, "bold") for k, v in BOLD_LOWER.items()},
    **{v: (k, "bold") for k, v in BOLD_DIGITS.items()},
    # Italic (mathematical)
    **{v: (k, "italic") for k, v in ITALIC_UPPER.items()},
    **{v: (k, "italic") for k, v in ITALIC_LOWER.items()},
    # Italic (sans-serif, used by some external tools)
    **{v: (k, "italic") for k, v in _SANS_SERIF_ITALIC_UPPER.items()},
    **{v: (k, "italic") for k, v in _SANS_SERIF_ITALIC_LOWER.items()},
    # Bold-Italic
    **{v: (k, "bold_italic") for k, v in BOLD_ITALIC_UPPER.items()},
    **{v: (k, "bold_italic") for k, v in BOLD_ITALIC_LOWER.items()},
    # Monospace
    **{v: (k, "monospace") for k, v in MONOSPACE_UPPER.items()},
    **{v: (k, "monospace") for k, v in MONOSPACE_LOWER.items()},
    **{v: (k, "monospace") for k, v in MONOSPACE_DIGITS.items()},
}

# ---------------------------------------------------------------------------
# Forward conversion helpers
# ---------------------------------------------------------------------------


def to_bold(text: str) -> str:
    """Convert ASCII text to Unicode Mathematical Sans-Serif Bold."""
    return "".join(
        BOLD_UPPER.get(c) or BOLD_LOWER.get(c) or BOLD_DIGITS.get(c) or c
        for c in text
    )


def to_italic(text: str) -> str:
    """Convert ASCII text to Unicode Mathematical Italic (letters only)."""
    return "".join(ITALIC_UPPER.get(c) or ITALIC_LOWER.get(c) or c for c in text)


def to_bold_italic(text: str) -> str:
    """Convert ASCII text to Unicode Mathematical Bold Italic."""
    return "".join(
        BOLD_ITALIC_UPPER.get(c) or BOLD_ITALIC_LOWER.get(c) or c for c in text
    )


def to_monospace(text: str) -> str:
    """Convert ASCII text to Unicode Mathematical Monospace."""
    return "".join(
        MONOSPACE_UPPER.get(c) or MONOSPACE_LOWER.get(c) or MONOSPACE_DIGITS.get(c) or c
        for c in text
    )


# ---------------------------------------------------------------------------
# Reverse conversion helpers
# ---------------------------------------------------------------------------


def strip_styling(text: str) -> str:
    """Strip all LinkedIn Unicode styling, returning plain ASCII text.

    Any character not in a styled Unicode block is passed through unchanged.
    """
    return "".join(_ALL_STYLED_TO_ASCII.get(c, (c, ""))[0] for c in text)


def char_style(c: str) -> str | None:
    """Return the style name for a styled Unicode character, or None if plain."""
    entry = _ALL_STYLED_TO_ASCII.get(c)
    return entry[1] if entry else None
