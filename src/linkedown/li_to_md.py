"""LinkedIn Unicode → Markdown converter.

This is an original addition to the linkedown package, contributed back to
the md-to-linkedin upstream project via PR. The reverse direction is
inherently heuristic: LinkedIn posts have no explicit structural metadata,
so headings, bold spans, and italic spans are inferred from context.

Heuristic rules applied (in order):
1. Lines whose *entire visible content* is bold Unicode → ``# Heading``
   (level 1 only; LinkedIn has no heading hierarchy).
2. Bullet lines (``• …``) → ``- …``
3. Blockquote lines (``│ …``) → ``> …``
4. Code-block lines (``▸ …``) → fenced ``` block
5. Thematic break line (``─…``) → ``---``
6. Inline bold spans  → ``**…**``
7. Inline italic spans → ``*…*``
8. Inline monospace spans → `` `…` ``
9. Link references ``text (url)`` → ``[text](url)``  (URL heuristic)
10. Image references ``[Image: alt] url`` → ``![alt](url)``
"""

from __future__ import annotations

import re
from typing import Final

from .unicode_maps import _ALL_STYLED_TO_ASCII, char_style, strip_styling

# ---------------------------------------------------------------------------
# Structural patterns
# ---------------------------------------------------------------------------

_BULLET_RE:     Final[re.Pattern[str]] = re.compile(r"^[•]\s+(.*)")
_QUOTE_RE:      Final[re.Pattern[str]] = re.compile(r"^│\s?(.*)")
_CODE_LINE_RE:  Final[re.Pattern[str]] = re.compile(r"^▸\s?(.*)")
_HRULE_RE:      Final[re.Pattern[str]] = re.compile(r"^─{3,}\s*$")
_IMAGE_REF_RE:  Final[re.Pattern[str]] = re.compile(r"^\[Image:\s*(.*?)\]\s+(\S+)\s*$")
# Link: "some text (https://example.com)" — only treat URLs in parens as links
_LINK_INLINE_RE: Final[re.Pattern[str]] = re.compile(
    r"(.*?)\s+\((https?://[^\s)]+)\)"
)

# ---------------------------------------------------------------------------
# Inline span reconstruction
# ---------------------------------------------------------------------------


def _spans_from_line(line: str) -> str:
    """Convert a line of possibly-styled Unicode text to Markdown inline syntax.

    Segments of consecutive characters sharing the same style are wrapped in
    the appropriate Markdown delimiter. Plain characters are emitted as-is.

    Style → delimiter mapping:
    - bold        → **…**
    - italic      → *…*
    - monospace   → `…`
    - bold_italic → ***…***   (best approximation)
    """
    if not line:
        return line

    # Build list of (char, style_or_None)
    segments: list[tuple[str, str | None]] = [
        (_ALL_STYLED_TO_ASCII.get(c, (c, None))[0], char_style(c)) for c in line
    ]

    # Maximum number of plain (neutral) characters allowed as a bridge between
    # two same-style spans.  Keeps " " and ", " inside a span while leaving
    # longer plain phrases (e.g. plain brand names like "oboe-mcp") outside.
    _MAX_BRIDGE = 4

    result: list[str] = []
    i = 0
    while i < len(segments):
        ascii_ch, style = segments[i]
        if style is None:
            result.append(ascii_ch)
            i += 1
        else:
            # Collect run of the same style, bridging short neutral gaps.
            j = i
            run_chars: list[str] = []
            while j < len(segments):
                ch, st = segments[j]
                if st == style:
                    run_chars.append(ch)
                    j += 1
                elif st is None:
                    # Peek ahead: collect the neutral gap, then check what follows.
                    gap: list[str] = []
                    k = j
                    while k < len(segments) and segments[k][1] is None:
                        gap.append(segments[k][0])
                        k += 1
                    # Bridge only if the gap is short and more same-style follows.
                    if (
                        k < len(segments)
                        and segments[k][1] == style
                        and len(gap) <= _MAX_BRIDGE
                    ):
                        run_chars.extend(gap)
                        j = k
                    else:
                        break
                else:
                    break  # Different style — end run.
            run_text = "".join(run_chars)
            delim = {
                "bold":        "**",
                "italic":      "*",
                "monospace":   "`",
                "bold_italic": "***",
            }.get(style, "")
            result.append(f"{delim}{run_text}{delim}")
            i = j

    return "".join(result)


# ---------------------------------------------------------------------------
# Line-level checks
# ---------------------------------------------------------------------------


def _is_all_bold(line: str) -> bool:
    """Return True if every alphanumeric character in *line* is bold Unicode."""
    has_alpha = False
    for c in line:
        if c.isspace() or not c.isascii() and c not in _ALL_STYLED_TO_ASCII:
            # structural punctuation — ignore
            continue
        style = char_style(c)
        if style is None and (c.isalpha() or c.isdigit()):
            return False  # plain alphanumeric → not a heading
        if style == "bold":
            has_alpha = True
        elif style is not None:
            return False  # mixed style → not a heading
    return has_alpha


# ---------------------------------------------------------------------------
# Block-level reconstruction helpers
# ---------------------------------------------------------------------------


def _flush_code(code_lines: list[str]) -> str:
    """Wrap accumulated code lines in a fenced block."""
    return "```\n" + "\n".join(code_lines) + "\n```\n"


def _apply_link_heuristic(text: str) -> str:
    """Convert 'label (url)' → '[label](url)' for HTTP/HTTPS URLs."""
    return _LINK_INLINE_RE.sub(r"[\1](\2)", text)


def _apply_image_heuristic(text: str) -> str:
    """Convert '[Image: alt] url' → '![alt](url)'."""
    return _IMAGE_REF_RE.sub(r"![\1](\2)", text)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def linkedin_to_md(text: str) -> str:
    """Convert LinkedIn Unicode-formatted text to Markdown.

    This conversion is heuristic. Structure (headings, lists, code blocks,
    blockquotes) is inferred from LinkedIn rendering conventions used by
    md-to-linkedin and similar tools. Inline bold/italic/monospace spans are
    reconstructed from Unicode block membership.

    Args:
        text: LinkedIn post text, potentially containing Unicode styled characters.

    Returns:
        Approximate Markdown equivalent of the input.
    """
    lines = text.splitlines()
    output: list[str] = []
    code_buffer: list[str] = []
    in_code_block = False

    for raw_line in lines:
        # --- Code block lines (▸) ---
        code_match = _CODE_LINE_RE.match(raw_line)
        if code_match:
            in_code_block = True
            code_buffer.append(code_match.group(1))
            continue

        # Flush code block when we leave code territory
        if in_code_block:
            output.append(_flush_code(code_buffer))
            code_buffer = []
            in_code_block = False

        # --- Thematic break ---
        if _HRULE_RE.match(raw_line):
            output.append("---\n")
            continue

        # --- Image reference ---
        if _IMAGE_REF_RE.match(raw_line):
            output.append(_apply_image_heuristic(raw_line) + "\n")
            continue

        # --- Blockquote ---
        quote_match = _QUOTE_RE.match(raw_line)
        if quote_match:
            inner = _spans_from_line(quote_match.group(1))
            output.append(f"> {inner}\n")
            continue

        # --- Bullet list ---
        bullet_match = _BULLET_RE.match(raw_line)
        if bullet_match:
            inner = _spans_from_line(bullet_match.group(1))
            inner = _apply_link_heuristic(inner)
            output.append(f"- {inner}\n")
            continue

        # --- Empty line ---
        if not raw_line.strip():
            output.append("\n")
            continue

        # --- Heading heuristic: entirely bold non-empty line ---
        if _is_all_bold(raw_line):
            plain = strip_styling(raw_line)
            output.append(f"# {plain}\n")
            continue

        # --- Regular paragraph line ---
        converted = _spans_from_line(raw_line)
        converted = _apply_link_heuristic(converted)
        converted = _apply_image_heuristic(converted)
        output.append(converted + "\n")

    # Flush any trailing code block
    if in_code_block and code_buffer:
        output.append(_flush_code(code_buffer))

    # Collapse runs of more than two blank lines
    result = re.sub(r"\n{3,}", "\n\n", "".join(output))
    return result.lstrip("\n")
