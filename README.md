# linkedown

Bidirectional **Markdown ↔ LinkedIn Unicode** converter.

LinkedIn does not render Markdown, but does display Unicode styled characters correctly.
`linkedown` converts between the two formats — both as a CLI tool and as an MCP server
for use by coding agents.

The Markdown → LinkedIn conversion logic is derived from
[md-to-linkedin](https://github.com/shenning00/md-to-linkedin) by Scott Henning (MIT).

## Installation

```sh
pip install linkedown
# or 
pipx install linkedown
```

## CLI usage

```sh
# Markdown → LinkedIn
md2li post.md                  # print to stdout
md2li post.md -o linkedin.txt  # write to file
md2li post.md --copy           # copy to clipboard

# LinkedIn → Markdown
li2md post.txt
li2md post.txt -o post.md

# Pipe
cat post.md | md2li
```

## MCP server

```sh
linkedown-mcp          # stdio server for Copilot/Claude/Codex/Cline
uvx linkedown linkedown-mcp
```

Tools exposed:
- `md_to_linkedin_tool` — Markdown → LinkedIn Unicode
- `linkedin_to_md_tool` — LinkedIn Unicode → Markdown

## Supported formatting

| Markdown       | LinkedIn output        |
|----------------|------------------------|
| `**bold**`     | 𝗯𝗼𝗹𝗱 (sans-serif bold)  |
| `*italic*`     | 𝘪𝘵𝘢𝘭𝘪𝘤               |
| `` `code` ``   | 𝚌𝚘𝚍𝚎 (monospace)       |
| `# Heading`    | **𝗛𝗲𝗮𝗱𝗶𝗻𝗴**            |
| `- item`       | • item                 |
| `` ``` `` block | ▸ prefixed lines      |
| `> quote`      | │ quote                |
| `[text](url)`  | text (url)             |
| `---`          | ─────────────          |

## License

MIT — see [LICENSE](LICENSE).

Attribution: Markdown → LinkedIn conversion logic derived from
[shenning00/md-to-linkedin](https://github.com/shenning00/md-to-linkedin) (MIT).
