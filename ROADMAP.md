# Project Roadmap

This roadmap outlines the planned development phases, feature releases, and architectural evolution of `well-document`.

---

## Phase 1: Core Skill & Governance Foundation (v1.0.0)

- [x] Master AI agent skill specification (`skills/well-document/SKILL.md`) for Cursor, Claude Code, Antigravity, and Windsurf.
- [x] Documentation anti-patterns catalog (`skills/well-document/references/anti-patterns.md`) codifying anti-AI-slop rules.
- [x] 4 repository interface archetypes (CLI, Library/SDK, Web/Backend, Monorepo).
- [x] 6-point pre-emit slop scorecard (`skills/well-document/references/slop-test.md`).
- [x] Portable POSIX installation script (`install.sh`).
- [x] Industry-standard open-source governance package (`README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`).

---

## Phase 2: Multi-Platform Distribution & Automated CI Governance (v1.1.0 - v1.3.0)

- [x] Skills CLI & npm registry package manifest (`package.json`) for `npx skills add AtaCanYmc/well-document`.
- [x] Windows PowerShell and CMD installer (`install.ps1`) alongside POSIX installer.
- [x] Cross-platform git normalization (`.gitattributes`) and universal editor configuration (`.editorconfig`).
- [x] GitHub issue forms (`bug_report.yml`, `feature_request.yml`), security routing (`config.yaml`), and pull request template.
- [x] GitHub CODEOWNERS for repository review assignment.
- [x] Markdownlint configuration (`.markdownlint.json`) and automated internal markdown link validation in CI.
- [x] Release Please automated CHANGELOG tracking and semantic release tagging.

---

## Phase 3: Agent Ecosystem Manifests & Advanced Tooling (v1.4.0) - Current

- [x] Native plugin manifests for Claude Code (`.claude-plugin/plugin.json`), Cursor (`.cursor-plugin/plugin.json`), and Antigravity (`plugin.json`).
- [x] Repository owner pull request auto-merge workflow (`.github/workflows/owner-auto-merge.yml`).
- [ ] GitHub Actions reusable workflow (`well-document-gate.yml`) to enforce anti-slop rules on incoming PRs.
- [ ] Pre-commit hook integration to verify codebase grounding before commit.

---

## Phase 4: Ecosystem Expansion & Multi-Language Adapters (v2.0.0) - Planned

- [ ] Specialized archetypes for Machine Learning repositories (Model cards, Weights & Biases configs, dataset checksums).
- [ ] Hardware & Embedded Systems archetype (schematics, pinouts, memory maps).
- [ ] Interactive terminal preview mode for local inspection before emission.
- [ ] Multi-lingual documentation synchronizer (strictly audited against machine translation slop).
