# Technical Architecture & Workflow Diagrams (Mermaid)

Modern GitHub markdown natively renders Mermaid.js diagrams. Instead of walls of text or external raster images that break on dark mode, use Mermaid to visualize architecture, control flow, and data lifecycles.

---

## When to Use Mermaid

Add a Mermaid diagram whenever documentation describes:
1. **System / Component Architecture**: High-level topologies, service boundaries, and internal module relationships.
2. **Request / Event Lifecycles**: How data moves between client, gateway, queue, workers, and storage.
3. **State Machines**: Order states, transaction lifecycle, connection states.
4. **CLI / Pipeline Workflows**: Build steps, CI checks, or release trains.

---

## Diagram Types & Best Practices

### 1. Flowcharts (`flowchart TD` / `flowchart LR`)
Use for component architecture and pipelines. Keep top-to-bottom (`TD`) for vertical workflows and left-to-right (`LR`) for pipelines.

```mermaid
flowchart LR
    Client["Client / SDK"] -->|"HTTPS POST /v1/events"| Gateway["API Gateway"]
    Gateway -->|"Verify HMAC"| Auth["Auth Engine"]
    Gateway -->|"Push Event"| Queue[("Redis Buffer")]
    Queue -->|"Batch Pull (100ms)"| Worker["Worker Daemon"]
    Worker -->|"Write Append-Only"| DB[("TimescaleDB")]
```

**Rules**:
- Wrap node labels containing punctuation, parentheses, or paths in double quotes: `A["Label (Detail)"]`.
- Use specific node shapes: `[Box]`, `(["Rounded"])`, `[("Database / Store")]`, `{"Decision"}`.
- Always label directional connections with explicit verbs or protocols: `-->|"HTTPS / REST"|`.

### 2. Sequence Diagrams (`sequenceDiagram`)
Use for protocols, authentication handshakes, and multi-actor interaction lifecycles.

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant CLI as CLI Tool
    participant API as Registry API
    participant Storage as S3 Storage

    Dev->>CLI: run publish --tag v1.0.0
    CLI->>API: POST /packages/auth (Token)
    API-->>CLI: 200 OK (Signed Upload URL)
    CLI->>Storage: PUT package.tar.gz
    Storage-->>CLI: 200 OK (ETag)
    CLI->>API: POST /packages/finalize
    API-->>CLI: 201 Created
    CLI-->>Dev: Successfully published v1.0.0
```

**Rules**:
- Always include `autonumber` for unambiguous step-by-step references in accompanying text.
- Differentiate between synchronous calls (`->>`), asynchronous messages (`-)`), and replies (`-->>`).

### 3. State Diagrams (`stateDiagram-v2`)
Use for finite state machines, connection lifecycles, and lifecycle transitions.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Connecting : Connect()
    Connecting --> Connected : Handshake OK
    Connecting --> Disconnected : Timeout
    Connected --> Processing : Message Received
    Processing --> Connected : ACK Sent
    Connected --> Disconnected : Connection Lost
    Disconnected --> Reconnecting : Auto-Retry (Exponential Backoff)
    Reconnecting --> Connected : Success
    Reconnecting --> Failed : Max Retries Exceeded
    Failed --> [*]
```

---

## Anti-AI-Slop Rules for Diagrams

1. **Max 10 Nodes**: Do not generate massive, unreadable 40-node spiderwebs. Focus on the core contract or subsystem being documented.
2. **No Fictional Entities**: Every service, database, or module in the diagram must physically correspond to a component in the codebase.
3. **No Unstyled Confetti**: Avoid random custom CSS classes or rainbow fills. Rely on GitHub's native theme styling or minimalist, high-contrast dark/light compatible node shapes.
4. **Readable in Both Dark and Light Themes**: Never force hardcoded white or black backgrounds on nodes that break theme switching.
