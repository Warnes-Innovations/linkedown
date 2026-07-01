# Codex Agent Instructions for linkedown

## What is linkedown?
A tool for converting Markdown to LinkedIn Unicode-styled text and back. Available as a CLI and MCP server.

## How to Use
- **CLI:**
	- Markdown → LinkedIn: `md2li input.md [-o output.txt] [--copy]`
	- LinkedIn → Markdown: `li2md input.txt [-o output.md]`
- **MCP Server:**
	- Start: `linkedown-mcp`
	- Tools: `md_to_linkedin_tool`, `linkedin_to_md_tool`

## Agent Integration
- Use CLI for local/manual conversion.
- Use MCP server for automated or agent workflows.
- Formatting rules and examples are in the README.

See agent-instructions/README.md for install steps.
