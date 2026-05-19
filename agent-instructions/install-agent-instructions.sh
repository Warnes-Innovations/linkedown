#!/bin/bash
# install-agent-instructions.sh — Install agent instructions for Copilot, Claude, Codex, and Cline
# SPDX-FileCopyrightText: 2024 Greg Warnes
# SPDX-License-Identifier: MIT

set -e

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Paths to agent instruction templates (assume they are in agent-instructions/)
INSTRUCTIONS_DIR="$SCRIPT_DIR"

# VS Code user data dir (macOS default)
VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"

# Ensure agent-instructions directory exists
if [ ! -d "$INSTRUCTIONS_DIR" ]; then
  echo "Error: agent-instructions/ directory not found in $SCRIPT_DIR."
  exit 1
fi

# Copy Copilot instructions
cp "$INSTRUCTIONS_DIR/copilot-instructions.md" "$VSCODE_USER_DIR/copilot-instructions.md"
echo "✓ Copilot instructions installed."

# Copy Claude instructions
cp "$INSTRUCTIONS_DIR/CLAUDE.md" "$VSCODE_USER_DIR/CLAUDE.md"
echo "✓ Claude instructions installed."

# Copy Codex instructions
cp "$INSTRUCTIONS_DIR/codex-instructions.md" "$VSCODE_USER_DIR/codex-instructions.md"
echo "✓ Codex instructions installed."

# Copy Cline instructions
cp "$INSTRUCTIONS_DIR/cline-instructions.md" "$VSCODE_USER_DIR/cline-instructions.md"
echo "✓ Cline instructions installed."

echo "All agent instructions installed."
