[← Back to Root Repository](../../README.md)

# well-document Skill Distribution

This directory contains the primary AI agent skill definition and reference knowledge bases for `well-document`.

---

## Table of Contents

- [Overview](#overview)
- [Directory Layout](#directory-layout)
- [Agent Loading & Invocations](#agent-loading--invocations)
- [Reference Index](#reference-index)

---

## Overview

The `skills/well-document/` directory is packaged to be mounted directly into AI coding assistant skill inventories (Google Antigravity, Gemini CLI, Claude Code, Cursor, Windsurf, and Codex). It provides deterministic anti-AI-slop instructions and evaluation scorecards.

---

## Directory Layout

```text
skills/well-document/
├── SKILL.md                 # Master skill prompt, verbs, and execution flow
└── references/              # Specialized knowledge bases loaded on demand
    ├── anti-patterns.md     # Catalog of AI-slop documentation tells & remediations
    ├── archetypes.md        # Layout standards for CLI, Library, Web, Monorepos, and Subfolders
    ├── automation.md        # CI/CD, Dependabot & Release Please integration standards
    ├── diagrams.md          # Technical Mermaid diagram standards & anti-slop rules
    ├── licensing.md         # Open-source legal triage & dependency compatibility matrix
    └── slop-test.md         # 6-point pre-emit audit scorecard
```

---

## Agent Loading & Invocations

When loaded into an AI coding assistant, the skill activates the following primary verbs:
- `well-document init`: Scans the repository and generates missing governance, documentation, and automation files.
- `well-document audit`: Evaluates existing documentation against the 6 evaluation gates without modifying files.
- `well-document polish <file>`: Rewrites a specific file to strip buzzword salad, emoji vomit, and unverified commands.
- `well-document recipes`: Outputs advanced CI and pre-commit automation recipes.

---

## Reference Index

- [`references/anti-patterns.md`](references/anti-patterns.md): Banned buzzwords, emoji rules, and hallucination preventions.
- [`references/archetypes.md`](references/archetypes.md): Document order for libraries, CLIs, web apps, monorepos, and subfolders.
- [`references/automation.md`](references/automation.md): GitHub Actions CI matrices, Dependabot, and Release Please.
- [`references/diagrams.md`](references/diagrams.md): Clean Mermaid flowchart, sequence, and state diagrams.
- [`references/licensing.md`](references/licensing.md): Copyleft infection triage and license compatibility.
- [`references/slop-test.md`](references/slop-test.md): 6-point pre-emit scorecard (G1–G6).
