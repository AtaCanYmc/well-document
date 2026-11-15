#!/usr/bin/env python3
"""
verify-anti-slop.py - Enforce Anti-AI-Slop Governance Gates
Detects marketing buzzword fluff, em-dash addiction, and unapproved emojis.
Zero external dependencies.
"""

import os
import re
import subprocess
import sys

FORBIDDEN_BUZZWORDS = [
    r"\bseamlessly\b",
    r"\bblazingly fast\b",
    r"\bcutting-edge\b",
    r"\brevolutionary\b",
    r"\bcomprehensive and robust\b",
    r"\beffortlessly\b",
]

FORBIDDEN_EMOJIS = [
    "🚀",
    "🔥",
    "✨",
    "🎉",
    "⚡",
]

# Patterns for lines discussing anti-patterns or quoting rules
EXCLUSION_PATTERNS = [
    r"strips meaningless",
    r"zero buzzword",
    r"banned buzzwords",
    r"catalog of ai-slop",
    r"forbidden=",
    r"anti-patterns in ai-generated",
    r"the anti-pattern",
    r"forbidden_buzzwords",
    r"anti-ai-slop",
    r"pre-emit scorecard",
]


def should_skip_line(line):
    lower = line.lower()
    return any(re.search(pat, lower) for pat in EXCLUSION_PATTERNS)


def get_files_to_check():
    """Detect files: arguments -> staged markdown files -> README.md."""
    if len(sys.argv) > 1:
        return [f for f in sys.argv[1:] if f.endswith(".md") and os.path.isfile(f)]

    try:
        cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
        staged = subprocess.check_output(cmd, text=True).splitlines()
        md_staged = [f for f in staged if f.endswith(".md") and os.path.isfile(f)]
        if md_staged:
            return md_staged
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    if os.path.isfile("README.md"):
        return ["README.md"]
    return []


def check_file(file_path):
    """Check a file for anti-slop violations."""
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Unable to read file: {e}"]

    in_code_block = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or should_skip_line(line):
            continue

        # Check for forbidden buzzwords
        for pat in FORBIDDEN_BUZZWORDS:
            if re.search(pat, line, re.IGNORECASE):
                violations.append(f"{file_path}:{idx}: Forbidden marketing buzzword matching '{pat}'")

        # Check for long dash (em-dash)
        if "—" in line:
            violations.append(f"{file_path}:{idx}: Forbidden long dash (em-dash '—') detected")

        # Check for unapproved emojis
        for emoji in FORBIDDEN_EMOJIS:
            if emoji in line:
                violations.append(f"{file_path}:{idx}: Unapproved emoji '{emoji}' detected")

    return violations


def main():
    files = get_files_to_check()
    if not files:
        print("verify-anti-slop: No files found to verify.")
        return 0

    total_violations = []
    for f in files:
        violations = check_file(f)
        total_violations.extend(violations)

    if total_violations:
        print("verify-anti-slop: FAILED. Found anti-slop violations:\n", file=sys.stderr)
        for v in total_violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print(f"verify-anti-slop: PASSED. Checked {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
