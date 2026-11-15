# Repository Documentation Archetypes

Every codebase has a primary interface. Match the documentation layout to the project's interface archetype instead of generating a one-size-fits-all template.

---

## 1. CLI Utility Archetype

Ideal for developer command-line tools, terminal utilities, and code generators.

### Section Order
1. **Header**: Name, one-sentence description, badges (License, CI, Release).
2. **Table of Contents**: Hyperlinked section index for fast keyboard/mouse navigation.
3. **Installation**: Zero-dependency preferred; direct binary curl / package manager snippet.
4. **Usage & Flags**: Immediate, executable command snippet followed by flag reference table.
5. **Configuration**: Config file format (YAML, TOML, JSON) with minimal required keys.
6. **Recipes**: Common shell pipeline workflows.

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
2. **Table of Contents**: Hyperlinked section navigation.
3. **Installation**: Package manager command (`pip install`, `npm i`, `cargo add`, `go get`).
4. **Minimal Code Example**: 10–15 lines of real, importable code solving a primary task.
5. **API Surface Overview**: Key structs, classes, or exported functions.
6. **Type Safety & Runtime Requirements**: Minimum compiler/runtime versions.

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
2. **Table of Contents**: Hyperlinked section navigation.
3. **System Architecture**: High-level Mermaid flowchart depicting service boundaries, ingress, and datastores.
4. **Quick Start (Docker / Turnkey Fast-Path)**: Shortest path to a running instance using Docker Compose.
5. **Manual Local Setup**: Alternative bare-metal setup for active development without containers.
6. **Environment Variables**: Table of required `.env` keys, types, and defaults.
7. **Database & Migrations**: Commands to migrate and seed the datastore.
8. **Testing & Verification**: Unit tests and healthcheck endpoint (`/healthz`).

```markdown
## Quick Start (Docker)

Launch the full stack including database and workers with a single command:

```bash
# 1. Clone and configure environment
git clone https://github.com/example/service.git && cd service
cp .env.example .env

# 2. Start services in background
docker compose up -d

# 3. Verify health
curl -f http://localhost:8080/healthz
```
```

---

## 4. Monorepo / Multi-Package Archetype

Ideal for multi-package repositories (Lerna, pnpm workspaces, Turborepo, Cargo workspaces).

### Section Order
1. **Header**: Workspace overview and package matrix.
2. **Table of Contents**: Hyperlinked section navigation.
3. **Workspace Topology**: Table mapping package name, directory path, and publish status.
4. **Dependency Graph**: Focused Mermaid flowchart mapping internal package dependencies.
5. **Root Commands**: How to bootstrap, build all, and run tests across workspaces.

---

## 5. Scoped Subfolder Archetype (Sub-packages, Modules, Workspaces)

Ideal for nested directories in monorepos (`packages/core`), sub-modules (`crates/parser`), internal utilities (`tools/benchmarks`), or skill directories (`skills/well-document`).

### Rules for Subfolder READMEs
1. **Never Duplicate Root Governance**: Do NOT duplicate `LICENSE`, `SECURITY.md`, or full contribution guides into subfolders. Reference the root.
2. **Top Breadcrumb Navigation**: Always begin with a backlink to the root repository: `[← Back to Root Repository](../../README.md)`.
3. **Table of Contents**: If the document spans more than 50 lines or 3 sections, include a hyperlinked Table of Contents.
4. **Local Scope**: Limit installation and usage examples to importing or compiling this specific submodule.

### Section Order
1. **Breadcrumb**: `[← Back to Root Repository](../../README.md)`
2. **Header**: Submodule name and technical purpose.
3. **Table of Contents**: (Mandatory if > 50 lines).
4. **Local Installation / Usage**: How to import, invoke, or link this specific subfolder.
5. **Public API Surface / Exports**: Key interfaces, structs, or functions exposed by this submodule.
6. **Local Verification**: How to run tests or linters scoped to this directory.

```markdown
[← Back to Root Repository](../../README.md)

# @scope/subpackage

High-throughput JSON stream tokenizer.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)

## Installation
pnpm add @scope/subpackage
```

---

## 6. Machine Learning & AI Repository Archetype

Ideal for model training repositories, fine-tuning scripts, model checkpoints, and evaluation suites (PyTorch, JAX, HuggingFace Transformers, vLLM).

### Section Order
1. **Header**: Model/pipeline purpose, architecture, parameter count, license (OpenRAIL/MIT/Apache-2.0).
2. **Table of Contents**: Hyperlinked section navigation.
3. **Model Card Summary**: Architecture, context length, parameter precision (FP16, BF16, INT8, INT4), supported tasks.
4. **Hardware & Runtime Requirements**: Minimum VRAM, CUDA/ROCm versions, disk requirements for weights.
5. **Quick Start (Inference)**: 10-line verbatim Python inference example (loading weights and tokenizer).
6. **Dataset Specifications & Integrity**: Splits (train/val/test), preprocessing instructions, and SHA-256 checksums table.
7. **Training & Fine-Tuning Pipeline**: Verbatim bash commands for single-GPU, DDP, or DeepSpeed runs.
8. **Telemetry & Experiment Tracking (W&B / MLflow)**: Configuration parameters, run naming, and offline logging flags.
9. **Evaluation Benchmarks**: Verifiable metric scorecard table (accuracy, perplexity, throughput tokens/sec) with reproduction scripts.

### Model Card Specification Table
| Parameter | Value | Description |
| :--- | :--- | :--- |
| Architecture | Decoder-only Transformer | Base model topology |
| Parameters | 7.2B (Active: 7.2B) | Total trainable weights |
| Precision | BF16 / FP16 | Native training precision |
| Context Window | 8,192 tokens | Maximum sequence length |
| Target Hardware | NVIDIA Ampere+ (>= 16GB VRAM) | Recommended inference hardware |

### Dataset Manifest & Checksums Table
| Dataset Split | Samples | Size | SHA-256 Checksum | Source |
| :--- | :--- | :--- | :--- | :--- |
| `train.parquet` | 1,200,000 | 4.2 GB | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Internal curated |
| `validation.parquet` | 50,000 | 180 MB | `ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb` | Benchmark split |

### Experiment Tracking Table (Weights & Biases / MLflow)
| Parameter | Env Variable / Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `project` | `WANDB_PROJECT` | `transformer-finetune` | Target W&B project dashboard |
| `entity` | `WANDB_ENTITY` | `team-ml` | Organizational workspace |
| `mode` | `WANDB_MODE` | `online` | Set `offline` for air-gapped clusters |
| `tags` | `--wandb-tags` | `baseline,bf16` | Comma-delimited experiment tags |

---

## 7. Hardware & Embedded Systems Archetype

Ideal for firmware repositories, bare-metal microcontrollers (STM32, ESP32, RP2040, Nordic nRF), FPGA designs, and robotics platforms (RTOS, embedded Rust, C/C++).

### Section Order
1. **Header**: Target hardware platform, core microcontroller architecture, firmware version.
2. **Table of Contents**: Hyperlinked section navigation.
3. **Hardware Specifications**: MCU, core clock speed, Flash, SRAM, operating voltage, peripheral bus clocking.
4. **Pinout & Peripheral Mapping**: Aligned tabular mapping of physical pins, alternate functions, bus interfaces, and connected peripherals.
5. **Memory Map & Partition Layout**: Flash sectors, SRAM regions, bootloader offsets, application partitions, and OTA slots.
6. **Toolchain & Prerequisites**: Required compilers (`arm-none-eabi-gcc`, `rustup target add`, `clang`), flashing probes (`probe-rs`, `openocd`, `esptool`, `J-Link`).
7. **Build & Flash Instructions**: Turnkey terminal commands to compile, flash over SWD/JTAG/UART, and attach serial monitor.
8. **Power & Environmental Constraints**: Input voltage limits, sleep/active power draw, thermal bounds.
9. **Schematics & PCB Artifacts**: Hardware revision history, KiCad/Gerber file links, and Bill of Materials (BOM) references.

### Pinout & Peripheral Mapping Table
| Pin | Alternate Function | Protocol / Signal | Connected Hardware | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `PA9` | `USART1_TX` | UART TX (115200 8N1) | Debug USB bridge | Console telemetry |
| `PA10` | `USART1_RX` | UART RX (115200 8N1) | Debug USB bridge | Command receiver |
| `PB6` | `I2C1_SCL` | I2C Clock (400 kHz) | BME280 Sensor | 4.7k pull-up installed |
| `PB7` | `I2C1_SDA` | I2C Data (400 kHz) | BME280 Sensor | 4.7k pull-up installed |
| `PC13` | `GPIO_Output` | Active-Low LED | Status LED | Heartbeat indicator |

### Flash & Memory Partition Layout Table
| Region | Start Address | End Address | Size | Access | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Bootloader | `0x08000000` | `0x08007FFF` | 32 KB | Read-Only | First-stage bootloader |
| Config Storage | `0x08008000` | `0x0800FFFF` | 32 KB | Read/Write | Non-volatile flash parameters |
| Application (Slot A) | `0x08010000` | `0x0807FFFF` | 448 KB | Read-Only | Active firmware binary |
| Application (Slot B) | `0x08080000` | `0x080EFFFF` | 448 KB | Read-Only | OTA staged firmware binary |

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

---

## Technical Tables for Structured Data

Never present structured configuration, environment variables, or CLI arguments as unstructured bullet points. Use compact, aligned markdown tables.

### 1. Environment Variables (`.env`) Schema
Always ground this table in actual keys found in `.env.example` or configuration parsers:

| Variable | Type | Default | Required | Description |
| :--- | :--- | :--- | :---: | :--- |
| `DATABASE_URL` | String (URI) | None | Yes | PostgreSQL connection URI. |
| `PORT` | Integer | `8080` | No | Ingress HTTP listener port. |
| `LOG_LEVEL` | Enum (`debug`, `info`, `warn`) | `info` | No | Logging verbosity filter. |
| `JWT_SECRET` | String (Base64) | None | Yes | Secret used to sign session tokens. |

### 2. CLI Options & Flags Schema
Use for command-line utilities and developer tools:

| Option / Flag | Short | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| `--target` | `-t` | Path | `.` | Target repository directory to inspect. |
| `--dry-run` | `-d` | Boolean | `false` | Preview operations without writing to disk. |
| `--force` | `-f` | Boolean | `false` | Overwrite existing governance files. |

### 3. Feature & Platform Compatibility Matrix
Use when differentiating editions, platform support, or runtime capabilities:

| Runtime / Engine | macOS (ARM64 / x86) | Linux (glibc / musl) | Windows (x64) |
| :--- | :---: | :---: | :---: |
| Python 3.10+ | Supported | Supported | Supported |
| Node.js 20+ | Supported | Supported | Supported |
| Native Go Binary | Supported | Supported | Supported |
