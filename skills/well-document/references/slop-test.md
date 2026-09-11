# Pre-Emit Slop Test & Audit Scorecard

Before committing or presenting generated documentation, audit the content against these 6 evaluation gates. Any score below 3 on any gate requires a revision pass.

---

## The 6 Evaluation Gates

| Gate | Category | Description | Pass Criteria (Score 4-5) | Fail Criteria (Score 1-2) |
| --- | --- | --- | --- | --- |
| **G1** | **Restraint** | Emoji & styling discipline | Max 1 neutral emoji per top-level heading; zero inline emojis. | Emojis in body text, rocket/fire/sparkle icons, excessive exclamation marks. |
| **G2** | **Verifiability** | Runnable instructions | All commands can be copied and run verbatim against the actual codebase. | Unresolvable packages, nonexistent script paths, undeclared env variables. |
| **G3** | **Specificity** | Precision of language | Direct description of algorithms, protocols, inputs, and outputs. | Buzzword salad ("revolutionary", "seamless", "blazingly fast", "robust"). |
| **G4** | **Grounding** | Codebase fidelity | File trees, package names, and modules correspond strictly to real files on disk. | Imaginary directories, hallucinated dependencies, fictional microservices. |
| **G5** | **Honesty** | Claims & social proof | Real benchmark methodology or no performance claims at all. | Made-up stats ("trusted by thousands", "+90% productivity boost"). |
| **G6** | **Governance** | Policies, license & contribution | Private security disclosure address, SLA, Conventional Commits, legally compatible license with real year & owner (zero bracket placeholders). | Blank security sections, incompatible license (e.g. MIT on GPL deps), bracket placeholders like `[year]` or `[fullname]`, vague rules. |

---

## Pre-Emit Stamp

When running in agent mode, self-score the generated artifact and prepend or record the evaluation:

```text
/* well-document · audit scorecard: G1:5 G2:5 G3:4 G4:5 G5:5 G6:5 · STATUS: PASS */
```
