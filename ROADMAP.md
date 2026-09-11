# Project Roadmap

This roadmap outlines the planned development phases, feature releases, and architectural evolution of `well-document`.

---

## Phase 1: Core Skill & Governance Foundation (v1.0.0) - Current

- [x] Master AI agent skill specification (`skills/well-document/SKILL.md`) for Cursor, Claude Code, Antigravity, and Windsurf.
- [x] Documentation anti-patterns catalog (`skills/well-document/references/anti-patterns.md`) codifying anti-AI-slop rules.
- [x] 4 repository interface archetypes (CLI, Library/SDK, Web/Backend, Monorepo).
- [x] 6-point pre-emit slop scorecard (`skills/well-document/references/slop-test.md`).
- [x] Portable POSIX installation script (`install.sh`).
- [x] Industry-standard open-source governance package (`README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`).

---

## Phase 2: Automation & CI Governance Gates (v1.1.0)

- [ ] GitHub Actions reusable workflow (`well-document-gate.yml`) to reject PRs containing AI slop or broken links.
- [ ] Pre-commit hook integration to prevent ungrounded file paths from being committed.
- [ ] Automatic package manifest badge generator (npm, crates.io, PyPI, Go Packages).
- [ ] Monorepo workspace linter verifying topology alignment.

---

## Phase 3: Ecosystem Expansion & Multi-Language Adapters (v2.0.0)

- [ ] Specialized archetypes for Machine Learning repositories (Model cards, Weights & Biases configs, dataset checksums).
- [ ] Hardware & Embedded Systems archetype (schematics, pinouts, memory maps).
- [ ] Interactive terminal preview mode for local inspection before emission.
- [ ] Multi-lingual documentation synchronizer (strictly audited against machine translation slop).
