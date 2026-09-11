# Anti-Patterns in AI-Generated Documentation

This document categorizes common "AI slop" patterns found in repository documentation and defines mandatory remediations.

---

## 1. Excessive and Playful Emojis

### The Anti-Pattern
Placing emojis inside technical sentences, bullet points, or badge lines:
> 🚀 *Supercharge your workflow with our blazing-fast ⚡️ and powerful 🔮 tool!* 🎉

### The Fix
Strip all inline emojis. Use clear, factual nouns and verbs:
> *A high-throughput queue processor built on POSIX shared memory.*

---

## 2. Empty Marketing Adjectives (Buzzword Salad)

### The Anti-Pattern
Using hyperbolic adjectives that convey zero technical specifications:
- *Seamless integration*
- *Blazingly fast*
- *Cutting-edge technology*
- *Revolutionary architecture*
- *Comprehensive and robust solution*
- *Effortless setup*

### The Fix
Replace with concrete technical parameters:
- Instead of *"blazingly fast"*, write: *"Sub-millisecond latency under 10k requests/sec."*
- Instead of *"seamless integration"*, write: *"Exposes a standard OpenTelemetry gRPC endpoint."*
- Instead of *"comprehensive solution"*, write: *"Handles retry backoff, dead-letter routing, and deduplication."*

---

## 3. Fabricated Social Proof & Imaginary Metrics

### The Anti-Pattern
Inventing adoption numbers or benchmarks that are not present in the repository code or test runs:
> *Trusted by 50,000+ developers across Fortune 500 companies.*
> *Reduces development cycles by 78%.*

### The Fix
Unless verified by independent data or committed benchmarks, state nothing. Ground every performance claim in a runnable script in `benchmarks/` or remove the claim entirely.

---

## 4. Hallucinated File Trees

### The Anti-Pattern
Outputting an idealized, generic project tree containing imaginary folders (`/core`, `/utils`, `/services`, `/config`) that do not exist in the user's codebase.

### The Fix
Run a directory scan before generating the tree. Display only directories and files that physically exist, or clearly delineate proposed scaffold items with a `[new]` tag.

---

## 5. Broken or Speculative Quick Starts

### The Anti-Pattern
Writing installation steps that reference unreleased packages (`pip install my-dream-tool`, `npm install @fantasy/core`), missing scripts (`./run.sh`), or undocumented environment variables without values.

### The Fix
- If the project is local, use editable install commands (`pip install -e .` or `npm link`).
- Document all environment variables with an explicit `.env.example` snippet.
- Verify every command in the quick start can execute without hanging.

---

## 6. Useless Section Padding

### The Anti-Pattern
- Multi-paragraph philosophical introductions explaining why the programming language is great.
- "Why Choose Us?" marketing grids with generic checkmarks.
- Empty FAQ sections containing trivial questions ("Is this free? Yes.").

### The Fix
Keep the README tight. A developer reading a GitHub repository needs:
1. What does it do? (1–2 sentences)
2. How do I install and run it? (Copy-paste code block)
3. What is the API / CLI interface? (Real examples)
4. Where are the architecture & contribution rules? (Links to docs)

---

## 7. Parenthetical Whispering & Long Dash Addiction

### The Anti-Pattern
Two telltale markers of AI-generated prose are endless parenthetical asides and chained long dashes (`—`):
> *The daemon — which runs in user space — buffers events (up to 10,000 entries) before committing to disk — ensuring persistent throughput (even under failure conditions).*

This creates hesitant, fragmented prose that reads like an LLM hedging its assertions.

### The Fix
1. **Ban Long Dashes (`—` / `--`)**: Eliminate em-dashes completely. Break compound thoughts into crisp, declarative sentences separated by periods.
2. **Minimize Parentheses**: Avoid using parentheses for explanatory clauses. If information is essential to the developer, write it directly in the main sentence. If it is non-essential, delete it entirely.

**Good Example**:
> *The daemon runs in user space. It buffers up to 10,000 events in memory before committing to disk to preserve throughput during disk latency spikes.*
