# Repository Documentation Archetypes

Every codebase has a primary interface. Match the documentation layout to the project's interface archetype instead of generating a one-size-fits-all template.

---

## 1. CLI Utility Archetype

Ideal for developer command-line tools, terminal utilities, and code generators.

### Section Order
1. **Header**: Name, one-sentence description, badges (License, CI, Release).
2. **Installation**: Zero-dependency preferred; direct binary curl / package manager snippet.
3. **Usage & Flags**: Immediate, executable command snippet followed by flag reference table.
4. **Configuration**: Config file format (YAML, TOML, JSON) with minimal required keys.
5. **Recipes**: Common shell pipeline workflows.

```markdown
# toolname

Deterministic code generator for POSIX systems.

## Installation
curl -fsSL https://get.toolname.dev | sh

## Usage
toolname build --input ./src --output ./dist
```

---

## 2. Library / SDK Archetype

Ideal for libraries, packages, client SDKs, and framework modules.

### Section Order
1. **Header**: Name, description, language version badges, package manager badge.
2. **Installation**: Package manager command (`pip install`, `npm i`, `cargo add`, `go get`).
3. **Minimal Code Example**: 10–15 lines of real, importable code solving a primary task.
4. **API Surface Overview**: Key structs, classes, or exported functions.
5. **Type Safety & Runtime Requirements**: Minimum compiler/runtime versions.

```markdown
# libname

Type-safe streaming client for Kafka and Redpanda.

## Quick Start
```python
from libname import StreamClient

client = StreamClient(broker="localhost:9092")
client.publish("events", payload={"status": "ok"})
```
```

---

## 3. Web Application / Backend Service Archetype

Ideal for full-stack apps, microservices, REST/GraphQL APIs, and worker daemons.

### Section Order
1. **Header**: Service purpose, architectural scope, status.
2. **System Architecture**: High-level Mermaid flowchart depicting service boundaries, ingress, and datastores.
3. **Local Environment Setup**: Prerequisites (Docker, PostgreSQL, Node/Python).
4. **Environment Variables**: Table of required `.env` keys, types, and defaults.
5. **Database & Migrations**: Commands to migrate and seed the datastore.
6. **Running Locally**: Dev server command, healthcheck URL (`/healthz`).
7. **Testing**: Unit and integration test execution.

---

## 4. Monorepo / Multi-Package Archetype

Ideal for multi-package repositories (Lerna, pnpm workspaces, Turborepo, Cargo workspaces).

### Section Order
1. **Header**: Workspace overview and package matrix.
2. **Workspace Topology**: Table mapping package name, directory path, and publish status.
3. **Dependency Graph**: Focused Mermaid flowchart mapping internal package dependencies.
4. **Root Commands**: How to bootstrap, build all, and run tests across workspaces.

---

## Conditional Section: Frequently Asked Questions (FAQ)

Not every repository needs an FAQ. Include an FAQ section **only** when the project meets at least two of the following conditions:
- There are established alternatives in the ecosystem (e.g. "Why X instead of Y?").
- The tool handles code, data, or credentials, raising natural privacy/telemetry questions (e.g. "Does this send data to external servers?").
- There are subtle architectural trade-offs or performance limitations developers need to know up front.
- Commercial or closed-source integration nuances need clarification.

### Rules for Technical FAQs
1. **No Trivial Fluff**: Never include questions like "Is this tool free?", "Why should I use this?", or generic marketing cheers.
2. **Concise, Concrete Answers**: Keep each answer between 2 and 5 sentences. Use bullet points or code references when explaining technical differences.
3. **Format**: Use standard markdown headers or collapsible `<details>` tags for longer Q&A sets.

```markdown
## Frequently Asked Questions

#### How does this differ from [Tool Y]?
Unlike [Tool Y], which requires a background daemon and centralized state, this library executes in-process with zero runtime dependencies.

#### Does this send any telemetry or code snippets off-machine?
No. All scanning and code generation runs strictly locally in memory. No network requests are initiated.

#### Can this be integrated into private/proprietary codebases?
Yes. The repository is licensed under the permissive MIT license, permitting proprietary and commercial embedding.
```
