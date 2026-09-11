# Contributing Guidelines

We welcome contributions to `well-document`. This project maintains strict engineering standards to ensure all generated governance rules and documentation remain clear, technically accurate, and free of AI-generated fluff.

---

## Code of Conduct

All participants agree to maintain professional, technical, and constructive interactions. Disagreements must be addressed with technical rationale, benchmarks, or reproducible examples.

---

## Contribution Workflow

### 1. Branch Naming

Create a feature branch from `main` using standard prefixes:
- `feat/<feature-name>`: New archetypes, rules, or generator features.
- `fix/<bug-name>`: Fixes for anti-patterns or template bugs.
- `docs/<subject>`: Documentation enhancements or new recipes.
- `refactor/<subject>`: Structural simplification or template refinement.

### 2. Commit Message Standards

We enforce [Conventional Commits (v1.0.0)](https://www.conventionalcommits.org/). Each commit message must follow this schema:

```text
<type>(<scope>): <short description>

[optional technical context / reasoning]
```

#### Allowed Types
- `feat`: New skill feature, archetype, or generator rule.
- `fix`: Bug fix in template rendering or detection.
- `docs`: Documentation, recipes, or guideline updates.
- `refactor`: Structural reorganization without functional changes.
- `test`: Addition or modification of verification tests.
- `chore`: Maintenance of build or deployment scripts.

#### Examples
- `feat(archetypes): add microservice backend template with docker compose`
- `fix(anti-patterns): include ungrounded benchmark detection rule`
- `docs(recipes): document GitHub Actions governance gate`

---

## Review & Pull Request Checklist

Before opening a Pull Request:
1. Ensure your edits conform to the anti-AI-slop rules in `skills/well-document/references/anti-patterns.md`.
2. Run the pre-emit verification scorecard (`skills/well-document/references/slop-test.md`). All 6 gates must score **4 or 5**.
3. Do not introduce frivolous emojis or buzzwords (*"seamless"*, *"blazingly fast"*).
4. Verify that any code snippets in `docs/` or `skills/well-document/references/` are syntactically valid and copy-paste executable.

---

## Pull Request Lifecycle

1. Open a PR against `main`.
2. Provide a clear summary of the changes and the rationale behind any modified rules.
3. Address review comments promptly. PRs adhering to the standards will be reviewed within 48 hours.
