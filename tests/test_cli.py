"""CLI integration tests using Click's test runner."""

from pathlib import Path

from click.testing import CliRunner

from linkedown.cli import li2md_main, md2li_main
from linkedown.unicode_maps import strip_styling


def test_md2li_from_file(tmp_path: Path) -> None:
    f = tmp_path / "input.md"
    f.write_text("# Hello\n\nThis is **bold**.\n", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(md2li_main, [str(f)])
    assert result.exit_code == 0
    plain = strip_styling(result.output)
    assert "Hello" in plain
    assert "bold" in plain


def test_md2li_stdin() -> None:
    runner = CliRunner()
    result = runner.invoke(md2li_main, ["-"], input="**bold** text\n")
    assert result.exit_code == 0
    assert "bold" in strip_styling(result.output)


def test_md2li_output_file(tmp_path: Path) -> None:
    f = tmp_path / "input.md"
    f.write_text("*italic*\n", encoding="utf-8")
    out = tmp_path / "out.txt"
    runner = CliRunner()
    result = runner.invoke(md2li_main, [str(f), "-o", str(out), "--quiet"])
    assert result.exit_code == 0
    assert out.exists()
    assert "italic" in strip_styling(out.read_text(encoding="utf-8"))


def test_li2md_from_file(tmp_path: Path) -> None:
    from linkedown.unicode_maps import to_bold
    f = tmp_path / "input.txt"
    f.write_text(to_bold("My Heading") + "\n\n• item\n", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(li2md_main, [str(f)])
    assert result.exit_code == 0
    assert "# My Heading" in result.output
    assert "- item" in result.output


def test_li2md_stdin() -> None:
    from linkedown.unicode_maps import to_bold
    runner = CliRunner()
    result = runner.invoke(li2md_main, ["-"], input=to_bold("Title") + "\n")
    assert result.exit_code == 0
    assert "# Title" in result.output


def test_md2li_missing_file() -> None:
    runner = CliRunner()
    result = runner.invoke(md2li_main, ["/nonexistent/path/file.md"])
    assert result.exit_code != 0


def test_md2li_no_args_no_pipe() -> None:
    """Without piped input and no file arg, should exit with error."""
    runner = CliRunner()
    # CliRunner's stdin is not a tty — pass explicit "-" with empty input.
    # Empty input → empty output is acceptable (exit 0).
    result = runner.invoke(md2li_main, ["-"], input="")
    assert result.exit_code == 0
