"""Command-line interface for linkedown.

Provides two entry points:
    md2li   — Markdown → LinkedIn Unicode
    li2md   — LinkedIn Unicode → Markdown

Both commands share the same input/output plumbing:

    <cmd> FILE          Read from file, write to stdout
    <cmd> -             Read from stdin, write to stdout
    <cmd> FILE -o OUT   Read from file, write to OUT
    <cmd> FILE --copy   Read from file, copy to clipboard
    cat f | <cmd>       Stdin → stdout (piped)
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from . import __version__, linkedin_to_md, md_to_linkedin

try:
    import pyperclip as _pyperclip
except ImportError:
    _pyperclip = None  # type: ignore[assignment]

console = Console()

# ---------------------------------------------------------------------------
# Shared I/O helpers
# ---------------------------------------------------------------------------


def _read(input_file: Optional[Path]) -> str:
    if input_file is None or str(input_file) == "-":
        if input_file is None and sys.stdin.isatty():
            raise click.UsageError(
                "No input file specified and stdin is not being piped. "
                "Pass a filename or pipe input via stdin."
            )
        return sys.stdin.read()
    if not input_file.exists():
        raise click.FileError(str(input_file), hint="File not found")
    if not input_file.is_file():
        raise click.FileError(str(input_file), hint="Path is not a file")
    return input_file.read_text(encoding="utf-8")


def _write(text: str, output_file: Optional[Path], copy: bool, quiet: bool) -> None:
    if copy:
        if _pyperclip is None:
            raise click.ClickException(
                "Clipboard support requires the 'pyperclip' package: "
                "pip install 'linkedown[clipboard]'"
            )
        _pyperclip.copy(text)
        if not quiet:
            console.print("[green]✓[/green] Copied to clipboard.")
        return

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(text, encoding="utf-8")
        if not quiet:
            console.print(f"[green]✓[/green] Written to {output_file}")
        return

    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")


# ---------------------------------------------------------------------------
# Shared Click options
# ---------------------------------------------------------------------------

_INPUT_ARG = click.argument(
    "input_file",
    type=click.Path(exists=False, path_type=Path),
    required=False,
)
_OUTPUT_OPT = click.option(
    "-o", "--output", "output_file",
    type=click.Path(path_type=Path),
    help="Write output to FILE instead of stdout.",
)
_COPY_OPT = click.option(
    "-c", "--copy", "copy_to_clipboard",
    is_flag=True,
    help="Copy output to clipboard (requires pyperclip).",
)
_QUIET_OPT = click.option(
    "-q", "--quiet",
    is_flag=True,
    help="Suppress informational messages.",
)


# ---------------------------------------------------------------------------
# md2li command
# ---------------------------------------------------------------------------


@click.command("md2li")
@_INPUT_ARG
@_OUTPUT_OPT
@_COPY_OPT
@_QUIET_OPT
@click.version_option(version=__version__, prog_name="md2li")
def md2li_main(
    input_file: Optional[Path],
    output_file: Optional[Path],
    copy_to_clipboard: bool,
    quiet: bool,
) -> None:
    """Convert Markdown to LinkedIn Unicode-formatted text.

    \b
    Examples:
        md2li post.md
        md2li post.md -o linkedin.txt
        md2li post.md --copy
        cat post.md | md2li
    """
    text = _read(input_file)
    result = md_to_linkedin(text)
    _write(result, output_file, copy_to_clipboard, quiet)


# ---------------------------------------------------------------------------
# li2md command
# ---------------------------------------------------------------------------


@click.command("li2md")
@_INPUT_ARG
@_OUTPUT_OPT
@_COPY_OPT
@_QUIET_OPT
@click.version_option(version=__version__, prog_name="li2md")
def li2md_main(
    input_file: Optional[Path],
    output_file: Optional[Path],
    copy_to_clipboard: bool,
    quiet: bool,
) -> None:
    """Convert LinkedIn Unicode-formatted text to Markdown.

    The conversion is heuristic: structure (headings, lists, code blocks)
    is inferred from LinkedIn rendering conventions. Results are generally
    clean for posts created with md2li or similar tools.

    \b
    Examples:
        li2md post.txt
        li2md post.txt -o post.md
        li2md post.txt --copy
        cat post.txt | li2md
    """
    text = _read(input_file)
    result = linkedin_to_md(text)
    _write(result, output_file, copy_to_clipboard, quiet)
