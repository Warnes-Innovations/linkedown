"""Markdown → LinkedIn Unicode converter.

Core conversion logic is derived from md-to-linkedin by Scott Henning
(https://github.com/shenning00/md-to-linkedin), MIT licence, with minor
adaptations for integration into linkedown.

Changes vs. upstream:
- Renderer and converter inlined here; no separate renderer.py
- ``convert()`` accepts the same ``options`` dict as upstream for compatibility
"""

from __future__ import annotations

import re
from typing import Any, Final, Optional

import mistune
from mistune.core import BlockState

from .unicode_maps import to_bold, to_italic, to_monospace

MAX_CONSECUTIVE_BLANK_LINES: Final[int] = 2


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------


class _LinkedInRenderer(mistune.BaseRenderer):
    """mistune renderer that converts Markdown tokens to LinkedIn Unicode text."""

    NAME = "linkedin"

    def __init__(self) -> None:
        super().__init__()

    def render_token(self, token: dict[str, Any], state: BlockState) -> str:
        func = self._get_method(token["type"])
        attrs = token.get("attrs")
        if "raw" in token:
            text = token["raw"]
        elif "children" in token:
            text = self.render_tokens(token["children"], state)
        else:
            return func(**attrs) if attrs else func()
        return func(text, **attrs) if attrs else func(text)

    def blank_line(self) -> str:
        return ""

    def block_text(self, text: str) -> str:
        return text

    def text(self, text: str) -> str:
        return text

    def heading(self, text: str, level: int, **_: Any) -> str:
        return f"{to_bold(text)}\n\n"

    def paragraph(self, text: str) -> str:
        return f"{text}\n\n"

    def emphasis(self, text: str) -> str:
        return to_italic(text)

    def strong(self, text: str) -> str:
        return to_bold(text)

    def codespan(self, text: str) -> str:
        return to_monospace(text)

    def block_code(self, code: str, info: Optional[str] = None) -> str:
        code = code.rstrip("\n")
        lines = [f"▸ {line}" for line in code.split("\n")]
        return "\n".join(lines) + "\n\n"

    def list(self, body: str, ordered: bool, **_: Any) -> str:
        return body + "\n"

    def list_item(self, text: str, **_: Any) -> str:
        return f"• {text.rstrip()}\n"

    def link(self, text: str, url: str, title: Optional[str] = None) -> str:
        return f"{text} ({url})"

    def image(self, alt: str, url: str, title: Optional[str] = None) -> str:
        return f"[Image: {alt}] {url}"

    def block_quote(self, text: str) -> str:
        text = text.rstrip("\n")
        lines = [f"│ {line}" for line in text.split("\n")]
        return "\n".join(lines) + "\n\n"

    def thematic_break(self) -> str:
        return "─────────────\n\n"

    def newline(self) -> str:
        return "\n"

    def linebreak(self) -> str:
        return "\n"

    def softbreak(self) -> str:
        return " "

    def inline_html(self, html: str) -> str:
        return html

    def raw_html(self, html: str) -> str:
        return html

    def strikethrough(self, text: str) -> str:
        return text

    def table(self, text: str) -> str:
        return text + "\n"

    def table_head(self, text: str) -> str:
        return text

    def table_body(self, text: str) -> str:
        return text

    def table_row(self, text: str) -> str:
        return text + "\n"

    def table_cell(self, text: str, **_: Any) -> str:
        return f"| {text} "


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def md_to_linkedin(markdown_text: str, options: Optional[dict[str, Any]] = None) -> str:
    """Convert Markdown text to LinkedIn-compatible Unicode-formatted text.

    Args:
        markdown_text: Standard Markdown input.
        options: Reserved for future configuration (ignored currently).

    Returns:
        LinkedIn-compatible plain-text with Unicode bold/italic/monospace.
    """
    renderer = _LinkedInRenderer()
    plugins = []
    try:
        plugins = ["strikethrough", "table"]
    except Exception:
        pass

    markdown = mistune.create_markdown(renderer=renderer, plugins=plugins)
    rendered = markdown(markdown_text)
    if not isinstance(rendered, str):
        raise TypeError(f"Expected str from renderer, got {type(rendered)}")
    return _post_process(rendered)


def _post_process(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    text = "\n".join(line.rstrip() for line in lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip("\n") + "\n"
