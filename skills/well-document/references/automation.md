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

Include `.github/workflows/release-please.yml` whenever Conventional Commits are used for versioned releases.

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
          release-type: simple
```

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
