#!/usr/bin/env sh
# well-document skill installer
# Installs well-document into supported AI agent skill directories.
set -eu

REPO_OWNER="AtaCanYmc"
REPO_NAME="well-document"
BRANCH="${WELL_DOCUMENT_BRANCH:-main}"
ARCHIVE_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/archive/refs/heads/${BRANCH}.tar.gz"

TMP_DIR=""
cleanup() {
  if [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT INT TERM

usage() {
  cat <<EOF
Usage: install.sh [OPTIONS] [CUSTOM_PATH]

Options:
  --antigravity, --gemini   Install for Google Antigravity / Gemini CLI
  --claude                  Install for Claude Code
  --cursor                  Install for Cursor
  --codex                   Install for OpenAI Codex / Copilot CLI
  --all                     Install for all supported AI agents
  -h, --help                Show this help message and exit

If no options are provided, existing agent directories are auto-detected.
EOF
}

resolve_source() {
  script_dir=""
  if [ -f "$0" ]; then
    script_dir="$(cd "$(dirname "$0")" && pwd)"
  fi

  if [ -n "$script_dir" ] && [ -f "$script_dir/skills/well-document/SKILL.md" ]; then
    REPO_ROOT="$script_dir"
    return 0
  fi

  echo "==> Downloading ${REPO_OWNER}/${REPO_NAME} (${BRANCH})..."
  TMP_DIR="$(mktemp -d)"

  if command -v curl >/dev/null 2>&1 && command -v tar >/dev/null 2>&1; then
    curl -fsSL "$ARCHIVE_URL" | tar -xz -C "$TMP_DIR"
    REPO_ROOT="${TMP_DIR}/${REPO_NAME}-${BRANCH}"
  elif command -v git >/dev/null 2>&1; then
    git clone --depth 1 --branch "$BRANCH" "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" "${TMP_DIR}/repo" >/dev/null 2>&1
    REPO_ROOT="${TMP_DIR}/repo"
  else
    echo "Error: curl+tar or git is required for remote installation." >&2
    exit 1
  fi

  if [ ! -f "${REPO_ROOT}/skills/well-document/SKILL.md" ]; then
    echo "Error: Could not locate skills/well-document/SKILL.md in downloaded archive." >&2
    exit 1
  fi
}

install_to() {
  dest="$1"
  name="$2"
  src_skill="${REPO_ROOT}/skills/well-document"
  src_scripts="${REPO_ROOT}/scripts"

  echo "==> Installing for ${name}: ${dest}"
  mkdir -p "${dest}/references"
  cp "${src_skill}/SKILL.md" "${dest}/SKILL.md"
  cp "${src_skill}/references/"*.md "${dest}/references/"

  if [ -d "$src_scripts" ]; then
    mkdir -p "${dest}/scripts"
    cp "${src_scripts}/"*.py "${dest}/scripts/" 2>/dev/null || true
  fi
}

# Parse help flag before downloading anything
for arg in "$@"; do
  case "$arg" in
    -h|--help)
      usage
      exit 0
      ;;
  esac
done

echo "==> well-document: AI Coding Assistant Skill Installer"
resolve_source

if [ $# -gt 0 ]; then
  for arg in "$@"; do
    case "$arg" in
      --antigravity|--gemini)
        install_to "${HOME}/.gemini/antigravity/skills/well-document" "Google Antigravity / Gemini"
        ;;
      --claude)
        install_to "${HOME}/.claude/skills/well-document" "Claude Code"
        ;;
      --codex)
        install_to "${HOME}/.codex/skills/well-document" "OpenAI Codex"
        ;;
      --cursor)
        install_to "${HOME}/.cursor/skills/well-document" "Cursor"
        ;;
      --all)
        install_to "${HOME}/.gemini/antigravity/skills/well-document" "Google Antigravity / Gemini"
        install_to "${HOME}/.claude/skills/well-document" "Claude Code"
        install_to "${HOME}/.cursor/skills/well-document" "Cursor"
        install_to "${HOME}/.codex/skills/well-document" "OpenAI Codex"
        ;;
      -*)
        echo "Error: Unknown option '$arg'. Run with --help for usage." >&2
        exit 1
        ;;
      *)
        install_to "$arg" "Custom path"
        ;;
    esac
  done
else
  installed=0
  if [ -d "${HOME}/.gemini" ]; then
    install_to "${HOME}/.gemini/antigravity/skills/well-document" "Google Antigravity / Gemini"
    installed=1
  fi
  if [ -d "${HOME}/.claude" ]; then
    install_to "${HOME}/.claude/skills/well-document" "Claude Code"
    installed=1
  fi
  if [ -d "${HOME}/.cursor" ]; then
    install_to "${HOME}/.cursor/skills/well-document" "Cursor"
    installed=1
  fi
  if [ -d "${HOME}/.codex" ]; then
    install_to "${HOME}/.codex/skills/well-document" "OpenAI Codex"
    installed=1
  fi

  if [ "$installed" -eq 0 ]; then
    install_to "${HOME}/.skills/well-document" "Default Agent Directory"
  fi
fi

echo "==> Installation complete. Skill active. Invoke with: well-document"
