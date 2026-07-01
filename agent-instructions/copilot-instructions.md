# Copilot Agent Instructions for linkedown

## Purpose
linkedown converts between Markdown and LinkedIn Unicode-styled text. Use it to prepare posts for LinkedIn or to recover Markdown from LinkedIn-formatted text.

## Usage
- **CLI:**
	- Markdown → LinkedIn: `md2li input.md [-o output.txt] [--copy]`
	- LinkedIn → Markdown: `li2md input.txt [-o output.md]`
- **MCP Server:**
	- Start: `linkedown-mcp`
	- Tools: `md_to_linkedin_tool`, `linkedin_to_md_tool`

## Agent Workflow
- Use the CLI for local file or clipboard conversion.
- Use the MCP server for programmatic conversion in agent workflows.
- For supported formatting, see the linkedown README.

## Example
```sh
md2li post.md --copy
li2md linkedin.txt -o post.md
```

See agent-instructions/README.md for install details.
