# Advanced Recipes & Integration Patterns

This document details battle-tested patterns for using and enforcing `well-document` across development teams and automated pipelines.

---

## Recipe 1: CI Governance Audit in GitHub Actions

Automatically verify that all repository documentation complies with anti-AI-slop rules on every Pull Request:

```yaml
name: Repository Documentation Audit

on:
  pull_request:
    paths:
      - '**.md'
      - '.github/**'

jobs:
  audit-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Verify Essential Governance Files
        run: |
          for file in README.md LICENSE CONTRIBUTING.md SECURITY.md; do
            if [ ! -f "$file" ]; then
              echo "Error: Missing required governance file: $file"
              exit 1
            fi
          done

      - name: Scan for Forbidden AI-Slop Buzzwords
        run: |
          FORBIDDEN="seamlessly|blazingly fast|cutting-edge|revolutionary|comprehensive and robust|effortlessly"
          if grep -E -i "$FORBIDDEN" README.md; then
            echo "Error: Forbidden marketing buzzwords detected in README.md"
            exit 1
          fi

      - name: Enforce Emoji Discipline in Body Text
        run: |
          # Fails if rocket, fire, or sparkle emojis appear
          if grep -P "[\x{1F680}\x{1F525}\x{2728}\x{1F389}]" README.md; then
            echo "Error: Unapproved emojis detected in README.md"
            exit 1
          fi
```

---

## Recipe 2: Prompting Agents with Custom Constraints

When directing an AI coding assistant (Cursor, Claude Code, Antigravity) to document a legacy repository, pass explicit parameters:

```text
Follow the well-document skill to document this repository.
Archetype: CLI Utility
Target Audience: Senior Systems Engineers
Strict Constraint: No marketing fluff, no speculative directories.
Every command in the Quick Start must execute locally with 'make test'.
```

---

## Recipe 3: Multi-Package Monorepo Mapping

When running `well-document` on a monorepo, include workspace topologies:

```markdown
### Workspace Topology

| Package | Directory | Type | Distribution |
| --- | --- | --- | --- |
| `@core/engine` | `packages/engine` | Library | Internal |
| `@cli/runner` | `packages/cli` | CLI Binary | Public (npm) |
| `@docs/site` | `apps/docs` | Static Site | Vercel |
```

---

## Recipe 4: Local Git Pre-Commit Hook

Install a pre-commit check to prevent committing ungrounded links:

```bash
#!/usr/bin/env sh
# .git/hooks/pre-commit
# Checks for broken markdown relative links

git diff --cached --name-only --diff-filter=ACM | grep '\.md$' | while read -r file; do
  # Extract markdown links like [text](path/to/file)
  grep -o '\[.*\]([a-zA-Z0-9_\/\.\-]*\.[a-zA-Z0-9]*)' "$file" | while read -r link; do
    target=$(echo "$link" | sed -E 's/.*\]\((.*)\)/\1/')
    if [ ! -e "$target" ] && [ ! -e "$(dirname "$file")/$target" ]; then
      echo "Pre-commit check failed: Broken link '$target' in $file"
      exit 1
    fi
  done
done
```
