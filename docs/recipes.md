# Advanced Recipes & Integration Patterns

This document details battle-tested patterns for using and enforcing `well-document` across development teams and automated pipelines.

---

## Recipe 1: Reusable CI Governance Gate in GitHub Actions

Automatically verify that all repository documentation complies with anti-AI-slop rules on every Pull Request using the reusable `well-document-gate.yml` workflow:

```yaml
name: Repository Governance Audit

on:
  pull_request:
    paths:
      - '**.md'
      - '.github/**'

jobs:
  governance-gate:
    uses: AtaCanYmc/well-document/.github/workflows/well-document-gate.yml@main
    with:
      check_governance: true
      check_slop: true
      check_links: true
      readme_path: "README.md"
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

## Recipe 4: Local Git Pre-Commit Hook Integration

Enforce codebase grounding and anti-slop rules on every staged commit before code reaches GitHub.

### Option A: Using the `pre-commit` Framework

Add `well-document` to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/AtaCanYmc/well-document
    rev: v1.3.0
    hooks:
      - id: well-document-grounding
      - id: well-document-anti-slop
```

Install and run:

```bash
pre-commit install
pre-commit run --all-files
```

### Option B: Standalone Verification Scripts

Run the bundled zero-dependency verification scripts directly in local git hooks or developer environments:

```bash
# Verify that relative links and file paths physically resolve
python3 scripts/verify-grounding.py

# Verify that staged markdown adheres to anti-slop constraints
python3 scripts/verify-anti-slop.py
```

---

## Recipe 5: Automated Owner PR Auto-Merge

Eliminate manual merge clicks for maintainer pull requests by queueing them for automatic squash-merge once CI status checks pass:

```yaml
name: Owner Auto-Merge

on:
  pull_request_target:
    types: [opened, synchronize, reopened, ready_for_review]
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.event.pull_request.user.login == github.repository_owner && !github.event.pull_request.draft
    steps:
      - name: Enable Auto-Merge for Owner PR
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_URL: ${{ github.event.pull_request.html_url }}
```
