# Security Policy

The `well-document` project maintains strict security standards for all codebase assets, dependencies, and generated governance files. This document details our version support matrix and the procedure for responsibly reporting security vulnerabilities.

---

## Supported Versions

Security fixes and patches are provided exclusively for active releases. Older versions are deprecated and unsupported.

| Version | Supported          | Security Advisory Status       |
| ------- | ------------------ | ------------------------------ |
| 1.x     | :white_check_mark: | Active support & triage        |
| < 1.0.0 | :x:                | Deprecated                     |

---

## Reporting a Security Vulnerability

If you discover a security vulnerability or suspect a security flaw in `well-document`, **do not open a public issue or discussion**. Public disclosure before a fix is prepared exposes the user community to unnecessary risk.

### Submission Channels

Please submit your report through one of the following private channels:

- **Email**: Send encrypted reports to `security@example.com`.
- **GitHub Private Vulnerability Reporting**: Use the **Report a vulnerability** tab under GitHub Security Advisories.

### What to Include in Your Report

To facilitate rapid evaluation and reproduction, please provide:

1. **Vulnerability Type**: Vulnerability class or policy violation (e.g. unsafe prompt injection in skill instructions, arbitrary local execution risk).
2. **Impact Assessment**: Affected components, severity rating, and potential attack scenarios.
3. **Reproduction Steps**: Step-by-step instructions or minimal reproduction prompt.
4. **Environment**: Operating system, AI agent/editor (Cursor, Claude Code, Antigravity), and `well-document` version.
5. **Remediation (Optional)**: Suggested rule patch or mitigation strategy.

---

## Response & Disclosure SLA

- **Acknowledgment**: Within **48 hours**, you will receive an initial response confirming receipt of your report.
- **Triage & Assessment**: Within **5 business days**, our security team will validate the issue, determine severity, and request any additional context.
- **Remediation & Patch**: An advisory and fix release will be prepared in a private fork.
- **Coordinated Disclosure**: Once the patch is published, the reporter will be credited in the release notes and advisory (unless anonymity is requested).
