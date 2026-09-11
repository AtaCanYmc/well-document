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
