# Copyright (c) 2026 Gregory R. Warnes
# SPDX-License-Identifier: MIT
"""linkedown MCP server.

Exposes two tools for use by coding agents:
    md_to_linkedin  — Convert Markdown text to LinkedIn Unicode-formatted text
    linkedin_to_md  — Convert LinkedIn Unicode text back to Markdown

Run as a standalone server:
    linkedown-mcp
    uvx linkedown linkedown-mcp
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import linkedin_to_md, md_to_linkedin

mcp = FastMCP(
    "linkedown",
    instructions=(
        "Tools for converting between Markdown and LinkedIn Unicode formatting. "
        "Use md_to_linkedin when preparing a post for LinkedIn. "
        "Use linkedin_to_md to convert existing LinkedIn text back to Markdown."
    ),
)


@mcp.tool()
def md_to_linkedin_tool(markdown_text: str) -> str:
    """Convert Markdown text to LinkedIn-compatible Unicode-formatted text.

    LinkedIn does not render Markdown, but does display Unicode styled characters
    correctly. This tool converts **bold**, *italic*, `code`, headings, lists,
    blockquotes, and code blocks to their LinkedIn-compatible equivalents.

    Args:
        markdown_text: Standard Markdown-formatted text.

    Returns:
        LinkedIn-compatible plain text with Unicode bold/italic/monospace styling.
    """
    return md_to_linkedin(markdown_text)


@mcp.tool()
def linkedin_to_md_tool(linkedin_text: str) -> str:
    """Convert LinkedIn Unicode-formatted text back to Markdown.

    Reconstructs Markdown structure (headings, lists, code blocks, blockquotes)
    and inline formatting (bold, italic, monospace) from LinkedIn Unicode characters.
    The conversion is heuristic: results are best for posts originally created
    from Markdown.

    Args:
        linkedin_text: Text copied from a LinkedIn post, containing Unicode styling.

    Returns:
        Approximate Markdown equivalent of the input.
    """
    return linkedin_to_md(linkedin_text)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
