#!/usr/bin/env sh
# well-document skill installer
# Installs well-document into supported AI agent skill directories.
set -eu

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$REPO_DIR/skills/well-document"

install_to() {
  dest="$1"
  name="$2"
  echo "==> Installing for $name: $dest"
  mkdir -p "$dest/references"
  cp "$SRC_DIR/SKILL.md" "$dest/SKILL.md"
  cp "$SRC_DIR/references/"*.md "$dest/references/"
}

echo "==> well-document: AI Coding Assistant Skill Installer"

if [ $# -gt 0 ]; then
  case "$1" in
    --antigravity|--gemini)
      install_to "$HOME/.gemini/antigravity/skills/well-document" "Google Antigravity / Gemini"
      ;;
    --claude)
      install_to "$HOME/.claude/skills/well-document" "Claude Code"
      ;;
    --codex)
      install_to "$HOME/.codex/skills/well-document" "OpenAI Codex"
      ;;
    --cursor)
      install_to "$HOME/.cursor/skills/well-document" "Cursor"
      ;;
    --all)
      install_to "$HOME/.gemini/antigravity/skills/well-document" "Google Antigravity / Gemini"
      install_to "$HOME/.claude/skills/well-document" "Claude Code"
      install_to "$HOME/.cursor/skills/well-document" "Cursor"
      install_to "$HOME/.codex/skills/well-document" "OpenAI Codex"
      ;;
    *)
      install_to "$1" "Custom path"
      ;;
  esac
else
  # Auto-detect existing environments or fallback to default
  installed=0
  if [ -d "$HOME/.gemini" ]; then
    install_to "$HOME/.gemini/antigravity/skills/well-document" "Google Antigravity / Gemini"
    installed=1
  fi
  if [ -d "$HOME/.claude" ]; then
    install_to "$HOME/.claude/skills/well-document" "Claude Code"
    installed=1
  fi
  if [ -d "$HOME/.cursor" ]; then
    install_to "$HOME/.cursor/skills/well-document" "Cursor"
    installed=1
  fi
  if [ -d "$HOME/.codex" ]; then
    install_to "$HOME/.codex/skills/well-document" "OpenAI Codex"
    installed=1
  fi

  if [ "$installed" -eq 0 ]; then
    install_to "$HOME/.skills/well-document" "Default Agent Directory"
  fi
fi

echo "==> Installation complete. Skill active. Invoke with: well-document"
