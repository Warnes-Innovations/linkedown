# Claude Agent Instructions for linkedown

## Overview
linkedown provides Markdown ↔ LinkedIn Unicode conversion as both a CLI and an MCP server.

### CLI Usage
- Convert Markdown to LinkedIn Unicode: `md2li input.md [-o output.txt] [--copy]`
- Convert LinkedIn Unicode to Markdown: `li2md input.txt [-o output.md]`

### MCP Server
- Start with: `linkedown-mcp`
- Exposes tools: `md_to_linkedin_tool`, `linkedin_to_md_tool`

### Agent Guidance
- Use CLI for file/clipboard conversion.
- Use MCP server for agent-driven conversion tasks.
- Refer to the README for formatting details and examples.

---
For installation, see agent-instructions/README.md.
