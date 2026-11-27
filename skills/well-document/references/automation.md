# CI/CD, Maintenance & Release Automation (GitHub Actions)

Modern open-source repositories automate code verification, dependency updates, and semantic version releases. An AI agent using `well-document` should scaffold these automations whenever the target repository has runnable test suites, linters, package manifests, or release targets.

---

## 1. Continuous Integration (CI) Workflows

### When to Include CI Workflows
Include `.github/workflows/ci.yml` whenever the codebase has:
- Unit / integration test suites (`tests/`, `__tests__/`, `*_test.go`, `tests.rs`).
- Linters, formatters, or static analyzers (Ruff, ESLint, Clippy, GolangCI-Lint).
- Compilers or build scripts (Cargo, Go, Maven, Gradle, TypeScript).
- Shell scripts or markdown documentation suites requiring syntax and link validation.

### Ecosystem CI Templates

#### A. Python CI (`.github/workflows/ci.yml`)
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          if [ -f pyproject.toml ]; then pip install -e .; fi
      - name: Run Tests
        run: python -m unittest discover -v
```

#### B. Node.js / TypeScript CI
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x, 22.x]

    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test --if-present
      - run: npm run build --if-present
```

#### C. Rust CI
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  check-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - run: cargo fmt --all -- --check
      - run: cargo clippy -- -D warnings
      - run: cargo test
```

#### D. Shell Script & Agent Skill CI (POSIX / Markdown)
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Shell Script Syntax
        run: |
          for f in $(find . -name "*.sh" -not -path "*/.*"); do
            sh -n "$f"
          done
      - name: Verify Essential Governance Files
        run: |
          for f in README.md LICENSE CONTRIBUTING.md SECURITY.md; do
            test -f "$f" || (echo "Missing $f" && exit 1)
          done
```

---

## 2. Automated Dependency Updates: Dependabot

Include `.github/dependabot.yml` whenever the repository uses package manifests or GitHub Actions.

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "chore(ci)"
    groups:
      github-actions:
        patterns:
          - "*"
```

---

## 3. Automated Changelogs & Releases: Release Please

Include `.github/workflows/release-please.yml`, `release-please-config.json`, and `.release-please-manifest.json` whenever Conventional Commits are used for versioned releases. Using manifest mode prevents version drift by synchronizing every version-bearing file across the repository on each release PR.

### Workflow (`.github/workflows/release-please.yml`)

```yaml
name: Release Please

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json
```

### Configuration (`release-please-config.json`)

Scan the repository for every manifest or metadata file containing a version field (`package.json`, `pyproject.toml`, `Cargo.toml`, `plugin.json`, `SKILL.md`, etc.) and register them under `extra-files` so a single release PR bumps all of them together:

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "simple",
      "changelog-path": "CHANGELOG.md",
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": true,
      "extra-files": [
        {
          "type": "json",
          "path": "package.json",
          "jsonpath": "$.version"
        },
        {
          "type": "json",
          "path": "plugin.json",
          "jsonpath": "$.version"
        },
        {
          "type": "generic",
          "path": "skills/well-document/SKILL.md"
        }
      ]
    }
  }
}
```

### Manifest (`.release-please-manifest.json`)

Initialize `.release-please-manifest.json` with the latest Git release tag (without the leading `v`):

```json
{
  ".": "1.0.0"
}
```

### Repo-Wide Version Sync Rules

1. **Zero Hardcoded Drift**: For non-JSON/TOML files tracked with `"type": "generic"` (such as `SKILL.md`, `README.md` version badges, or shell constants), place an inline `# x-release-please-version` marker on the version line so Release Please updates it automatically.
2. **Tag Alignment**: Before scaffolding `.release-please-manifest.json`, check `git tag --sort=-v:refname | head -n 1` and seed the manifest with the actual latest tag.
3. **Matching `release-type`**: Set `release-type` to match the primary ecosystem (`node`, `python`, `rust`, `go`, or `simple`) and keep secondary manifests in `extra-files`.

---

## 4. README Badge Rule

When a CI workflow is scaffolded, always place the corresponding GitHub Actions status badge in the `README.md` badge bar:

```markdown
[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)
```

---

## 5. Issue Templates & Config (`.github/ISSUE_TEMPLATE/`)

Every production open-source repository requires structured issue templates to reject incomplete bug reports, direct security disclosures to private channels, and structure feature proposals.

Scaffold the directory `.github/ISSUE_TEMPLATE/` with `config.yaml`, `bug_report.yml`, and `feature_request.yml`.

### A. Issue Configuration (`.github/ISSUE_TEMPLATE/config.yaml`)
Disables blank issues to enforce structured input and routes security inquiries to the security policy.

```yaml
blank_issues_enabled: false
contact_links:
  - name: Security Vulnerabilities
    url: https://github.com/OWNER/REPO/security/policy
    about: Please report security vulnerabilities privately according to our security policy.
  - name: Community & Questions
    url: https://github.com/OWNER/REPO/discussions
    about: Ask questions and discuss feature ideas with the community.
```

### B. Bug Report Form (`.github/ISSUE_TEMPLATE/bug_report.yml`)
Enforces reproduction steps, environment details, and execution logs.

```yaml
name: Bug Report
description: Report a reproducible defect or bug
title: "fix: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Please verify the issue has not been reported before opening a new ticket.
        For security vulnerability reports, refer to [SECURITY.md](../../SECURITY.md).
  - type: textarea
    id: summary
    attributes:
      label: Bug Description
      description: Provide a clear and concise description of the bug.
      placeholder: Describe what happened.
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Step-by-step instructions to reproduce the behavior.
      placeholder: |
        1. Run command '...'
        2. Inspect output '...'
        3. Observe error '...'
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs or Terminal Output
      description: Paste relevant terminal output or stack traces.
      render: shell
  - type: input
    id: environment
    attributes:
      label: Environment
      description: OS version, runtime version, package version.
      placeholder: macOS 14.5, Node 20.10.0, etc.
    validations:
      required: true
```

### C. Feature Request Form (`.github/ISSUE_TEMPLATE/feature_request.yml`)
Frames proposals around technical problems, expected behavior, and architectural alternatives.

```yaml
name: Feature Request
description: Propose a new feature, improvement, or architectural change
title: "feat: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Please check existing issues and roadmaps to ensure this proposal is not already tracked.
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: Describe the technical friction or limitation this feature resolves.
      placeholder: I encounter an issue when...
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposed Solution
      description: Detail the requested behavior or API changes.
      placeholder: Add support for...
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Describe any alternative solutions or workarounds you considered.
  - type: checkboxes
    id: checklist
    attributes:
      label: Contributor Checklist
      options:
        - label: I searched existing issues and PRs before submitting this request.
          required: true
        - label: This proposal adheres to anti-AI-slop and governance standards.
          required: true
```

---

## 6. Pull Request Template (`.github/PULL_REQUEST_TEMPLATE/`)

Standardizes pull request descriptions, links changes to Conventional Commits, and requires explicit verification commands before merging.

Scaffold `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`:

```markdown
## Description

<!-- Provide a concise technical summary of the changes introduced in this PR. -->

## Changes

<!-- List specific files, functions, or configurations modified. -->
- 

## Type of Change

- [ ] `feat`: New capability, archetype, or rule
- [ ] `fix`: Bug fix or corrective refinement
- [ ] `docs`: Documentation updates or additions
- [ ] `refactor`: Code or structure refinement without behavioral changes
- [ ] `test`: New or updated tests
- [ ] `chore`: Tooling, CI, or dependency updates

## Verification

<!-- Detail the steps taken to verify the changes locally or in CI. -->

```bash
# Reproduction or test commands executed
```

## Checklist

- [ ] My commits adhere to [Conventional Commits](https://www.conventionalcommits.org/).
- [ ] Documentation has been updated to reflect the changes.
- [ ] No extraneous dependencies, temporary files, or AI slop introduced.
- [ ] All tests and CI validations pass locally.
```

---

## 7. Markdown Linting (`.markdownlint.json`)

To prevent formatting drift, heading skips, and whitespace defects in documentation without breaking tables or Mermaid blocks, scaffold `.markdownlint.json` in the repository root:

```json
{
  "default": true,
  "MD013": false,
  "MD033": {
    "allowed_elements": [
      "img",
      "details",
      "summary",
      "div",
      "p"
    ]
  },
  "MD024": {
    "siblings_only": true
  },
  "MD041": false
}
```

### Key Rule Rationale
- `MD013` (Line length): Disabled to avoid breaking Markdown tables, long URLs, and Mermaid code fences.
- `MD033` (Inline HTML): Relaxed specifically for images (banners/badges) and `<details>` collapsible recipe blocks.
- `MD024` (Multiple headings with identical text): Permitted under different parent sections (e.g. duplicate `### Example` or `### Step` subheadings).
- `MD041` (First line must be top-level heading): Disabled to allow top banners, navigation breadcrumbs, and badge bars above the main `# Heading`.

---

## 8. Cross-Platform Git Normalization (`.gitattributes`)

Repositories supporting multi-platform development require deterministic line endings to prevent shell script execution failures on Unix/Docker and preserve binary assets.

Scaffold `.gitattributes` in the repository root:

```gitattributes
# Auto detect text files and perform LF normalization on checkout
* text=auto eol=lf

# Explicit shell script normalization (strictly LF across Windows, macOS, Linux)
*.sh text eol=lf
*.bash text eol=lf
*.zsh text eol=lf

# PowerShell scripts (support Windows execution while keeping normalized text)
*.ps1 text eol=crlf
*.psm1 text eol=crlf
*.psd1 text eol=crlf

# Documentation & Structured Data
*.md text diff=markdown
*.json text
*.yml text
*.yaml text

# Binary assets (avoid corruption or line-ending conversions)
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.svg text
*.pdf binary

# Release Archive Exclusions (keep distribution tarballs clean)
.github export-ignore
.gitignore export-ignore
.gitattributes export-ignore
```

### Key Technical Mechanics
- `eol=lf`: Enforces Unix line endings so POSIX shell scripts (`install.sh`, CI scripts) do not crash when cloned on Windows.
- `diff=markdown`: Optimizes `git diff` output to display Markdown headings and structural changes accurately.
- `binary`: Prevents accidental line-ending conversions and corruptions on images and icons.
- `export-ignore`: Excludes internal CI, issue templates, and git configuration from release archives produced by `git archive`.

---

## 9. Universal Editor Configuration (`.editorconfig`)

Ensure cross-editor formatting consistency (VS Code, Cursor, JetBrains, Vim) without requiring manual plugin configuration.

Scaffold `.editorconfig` in the repository root:

```ini
# http://editorconfig.org
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_size = 4

[*.{sh,bash,zsh}]
indent_size = 2
end_of_line = lf

[*.{ps1,psm1,psd1}]
indent_size = 4
end_of_line = crlf

[*.md]
trim_trailing_whitespace = false
```

---

## 10. Code Ownership & PR Routing (`.github/CODEOWNERS`)

Direct pull request reviews automatically to authorized maintainers or subsystem teams.

Scaffold `.github/CODEOWNERS`:

```text
# Global code ownership
* @OWNER

# Workflows and automation manifests
/.github/ @OWNER

# Security, licensing, and governance
/LICENSE @OWNER
/SECURITY.md @OWNER
/CONTRIBUTING.md @OWNER
```

---

## 11. Internal Documentation Link Validation (CI)

Prevent broken markdown links and dead relative anchors from decaying repository documentation over time.

Add to `.github/workflows/ci.yml`:

```yaml
      - name: Validate Internal Documentation Links
        run: |
          python3 -c '
          import re, glob, os

          def check_file(f):
              content = open(f, encoding="utf-8").read()
              # Strip code fences and inline spans to avoid false matches
              content = re.sub(r"```[\s\S]*?```", "", content)
              content = re.sub(r"`[^`]*`", "", content)
              links = re.findall(r"\[.*?\]\((?!https?://|mailto:)(.*?)(?:#.*)?\)", content)
              broken = []
              for link in links:
                  link = link.strip()
                  if not link or link.startswith("#"): continue
                  target = os.path.normpath(os.path.join(os.path.dirname(f), link))
                  if not os.path.exists(target):
                      broken.append(f"{f} -> {link} (resolved: {target})")
              return broken

          all_broken = []
          for f in glob.glob("**/*.md", recursive=True):
              all_broken.extend(check_file(f))

          if all_broken:
              print("Error: Broken internal documentation links detected:")
              for b in all_broken:
                  print("  -", b)
              exit(1)
          print("Internal documentation links verified.")
          '
```

---

## 12. Owner PR Auto-Merge (`.github/workflows/owner-auto-merge.yml`)

For repositories where maintainers iterate via feature branches, manually merging personal pull requests after CI checks pass adds repetitive overhead.

Scaffold `.github/workflows/owner-auto-merge.yml` to queue pull requests authored by the repository owner for automated squash-merging once all required CI checks pass:

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

### Technical Rules & Guardrails
- **Status Checks Preserved**: The native GitHub auto-merge queue does not bypass tests or branch protections. Merging occurs only after all status checks succeed.
- **Strict Identity Enforcement**: The guard `github.event.pull_request.user.login == github.repository_owner` ensures external contributor and third-party PRs are never auto-merged.
- **Draft Safeguard**: Draft pull requests are ignored until explicitly marked ready for review.
- **Repository Setting Prerequisite**: In GitHub repository **Settings** -> **General** -> **Pull Requests**, check **Allow auto-merge**. Under **Settings** -> **Actions** -> **General** -> **Workflow permissions**, verify **Allow GitHub Actions to create and approve pull requests** is enabled.

---

## 13. Dependabot Auto-Merge (`.github/workflows/dependabot-auto-merge.yml`)

When `.github/dependabot.yml` is present, manually approving and merging routine `patch` and `minor` dependency updates creates unnecessary maintenance toil.

Scaffold `.github/workflows/dependabot-auto-merge.yml` to automatically approve and queue `patch` and `minor` Dependabot PRs for squash-merging once all required CI checks pass:

```yaml
name: Dependabot Auto-Merge

on:
  pull_request_target:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  dependabot:
    runs-on: ubuntu-latest
    if: github.event.pull_request.user.login == 'dependabot[bot]'
    steps:
      - name: Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"

      - name: Approve and enable auto-merge for minor and patch updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-minor' || steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: |
          gh pr review --approve "$PR_URL"
          gh pr merge --auto --squash "$PR_URL"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_URL: ${{ github.event.pull_request.html_url }}
```

### Technical Rules & Guardrails
- **Semver Guard**: Only `semver-minor` and `semver-patch` updates are auto-approved and queued. `semver-major` updates still require manual review to catch breaking changes.
- **Strict Identity Enforcement**: `github.event.pull_request.user.login == 'dependabot[bot]'` ensures only authentic Dependabot PRs trigger the workflow.
- **Status Checks Preserved**: `gh pr merge --auto --squash` waits for all required CI status checks and branch protection rules before merging.
- **Repository Setting Prerequisite**: Requires **Allow auto-merge** and **Allow GitHub Actions to create and approve pull requests** in repository settings.

---

## 13. Reusable Governance Gate (`.github/workflows/well-document-gate.yml`)

Repositories adopting `well-document` can centralize anti-slop verification into a reusable GitHub Actions workflow. This enables downstream repositories to inherit governance checks via a clean caller job.

### Reusable Workflow Definition
```yaml
name: Well Document Governance Gate

on:
  workflow_call:
    inputs:
      check_governance:
        description: "Verify essential governance files"
        required: false
        type: boolean
        default: true
      check_slop:
        description: "Enforce anti-AI-slop rules"
        required: false
        type: boolean
        default: true
      check_links:
        description: "Validate internal markdown relative links"
        required: false
        type: boolean
        default: true
      readme_path:
        description: "Path to root README file"
        required: false
        type: string
        default: "README.md"

jobs:
  gate:
    name: Anti-Slop & Governance Gate
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Verify Essential Governance Files
        if: ${{ inputs.check_governance }}
        run: |
          for f in "${{ inputs.readme_path }}" LICENSE CONTRIBUTING.md SECURITY.md ROADMAP.md; do
            if [ ! -f "$f" ]; then
              echo "::error file=$f::Missing required governance file: $f"
              exit 1
            fi
          done

      - name: Run Anti-AI-Slop Linter
        if: ${{ inputs.check_slop }}
        run: |
          README_FILE="${{ inputs.readme_path }}"
          FORBIDDEN="seamlessly|blazingly fast|cutting-edge|revolutionary|comprehensive and robust|effortlessly"
          SLOP_MATCHES=$(grep -E -i "$FORBIDDEN" "$README_FILE" | grep -v -E "Strips meaningless|Zero Buzzword" || true)
          if [ -n "$SLOP_MATCHES" ]; then
            echo "::error file=$README_FILE::Forbidden marketing buzzwords found in documentation"
            exit 1
          fi
          if grep -q "—" "$README_FILE"; then
            echo "::error file=$README_FILE::Forbidden long dash (em-dash) detected"
            exit 1
          fi

      - name: Validate Codebase Grounding & Links
        if: ${{ inputs.check_links }}
        run: |
          python3 -c '
          import re, glob, os, sys
          broken = []
          for f in glob.glob("**/*.md", recursive=True):
              content = re.sub(r"```[\s\S]*?```", "", open(f, encoding="utf-8").read())
              content = re.sub(r"`[^`]*`", "", content)
              for link in re.findall(r"\[.*?\]\((?!https?://|mailto:)(.*?)(?:#.*)?\)", content):
                  link = link.strip().split("?")[0]
                  if not link or link.startswith("#"): continue
                  target = os.path.normpath(os.path.join(os.path.dirname(f), link))
                  if not os.path.exists(target):
                      broken.append(f"{f} -> {link}")
          if broken:
              print("Broken links detected:", broken, file=sys.stderr)
              sys.exit(1)
          '
```

### Caller Workflow Example
```yaml
jobs:
  governance:
    uses: AtaCanYmc/well-document/.github/workflows/well-document-gate.yml@main
```

---

## 14. Pre-Commit Hook Integration (`.pre-commit-hooks.yaml`)

To catch ungrounded paths and anti-slop violations before commit creation, repositories can expose hooks compatible with the `pre-commit` framework.

### Hook Manifest (`.pre-commit-hooks.yaml`)
```yaml
- id: well-document-grounding
  name: Verify Codebase Grounding
  description: Verifies that relative links and file paths in staged markdown files physically exist on disk.
  entry: scripts/verify-grounding.py
  language: python
  types: [markdown]
  pass_filenames: true

- id: well-document-anti-slop
  name: Anti-AI-Slop Linter
  description: Scans staged documentation for forbidden marketing buzzwords, em-dashes, and unapproved emojis.
  entry: scripts/verify-anti-slop.py
  language: python
  types: [markdown]
  pass_filenames: true
```

### Consumer Configuration (`.pre-commit-config.yaml`)
```yaml
repos:
  - repo: https://github.com/AtaCanYmc/well-document
    rev: v1.3.0
    hooks:
      - id: well-document-grounding
      - id: well-document-anti-slop
```
