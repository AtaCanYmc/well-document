#!/usr/bin/env python3
"""
preview.py - Interactive Terminal Markdown Preview & Pre-Emit Inspector
Renders structured markdown in the terminal with ANSI styling and runs
real-time audit scorecard evaluation. Zero external dependencies.
"""

import argparse
import difflib
import os
import re
import sys

# ANSI Colors
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


def disable_colors():
    global BOLD, DIM, CYAN, GREEN, YELLOW, RED, MAGENTA, RESET
    BOLD = DIM = CYAN = GREEN = YELLOW = RED = MAGENTA = RESET = ""


FORBIDDEN_BUZZWORDS = [
    r"\bseamlessly\b",
    r"\bblazingly fast\b",
    r"\bcutting-edge\b",
    r"\brevolutionary\b",
    r"\bcomprehensive and robust\b",
    r"\beffortlessly\b",
]

FORBIDDEN_EMOJIS = ["🚀", "🔥", "✨", "🎉", "⚡"]


def evaluate_document(content, file_path=""):
    """Evaluate document against the 6 well-document audit gates."""
    scores = {}
    notes = []

    # G1: Restraint (em-dashes, unapproved emojis)
    em_dashes = len(re.findall(r"—", content))
    emojis = [e for e in FORBIDDEN_EMOJIS if e in content]
    g1_score = 5
    if em_dashes > 0:
        g1_score = max(1, g1_score - em_dashes * 2)
        notes.append(f"G1 Restraint: {em_dashes} forbidden em-dash ('—') occurrences found.")
    if emojis:
        g1_score = max(1, g1_score - len(emojis) * 2)
        notes.append(f"G1 Restraint: Unapproved emojis detected ({', '.join(emojis)}).")
    scores["G1"] = g1_score

    # G2: Verifiability (code blocks present and non-empty)
    code_blocks = re.findall(r"```([a-zA-Z0-9_\-]+)?\n([\s\S]*?)```", content)
    g2_score = 5 if code_blocks else 3
    if not code_blocks:
        notes.append("G2 Verifiability: No fenced code blocks found in document.")
    scores["G2"] = g2_score

    # G3: Specificity (buzzwords)
    buzzword_hits = []
    # Ignore explicit anti-pattern catalogs
    filtered_content = "\n".join(
        line for line in content.splitlines()
        if not re.search(r"zero buzzword|strips meaningless|forbidden buzzword|anti-pattern", line, re.IGNORECASE)
    )
    for pat in FORBIDDEN_BUZZWORDS:
        if re.search(pat, filtered_content, re.IGNORECASE):
            buzzword_hits.append(pat.replace(r"\b", ""))
    g3_score = 5
    if buzzword_hits:
        g3_score = max(1, 5 - len(buzzword_hits) * 2)
        notes.append(f"G3 Specificity: Forbidden marketing buzzwords: {', '.join(buzzword_hits)}.")
    scores["G3"] = g3_score

    # G4: Grounding (relative links exist on disk)
    broken_links = []
    base_dir = os.path.dirname(os.path.abspath(file_path)) if file_path else os.getcwd()
    clean_text = re.sub(r"```[\s\S]*?```", "", content)
    clean_text = re.sub(r"`[^`]*`", "", clean_text)
    links = re.findall(r"\[.*?\]\((?!https?://|mailto:)(.*?)\)", clean_text)
    for raw_link in links:
        target = raw_link.split("#")[0].split("?")[0].strip()
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(base_dir, target))
        if not os.path.exists(resolved):
            broken_links.append(target)
    g4_score = 5
    if broken_links:
        g4_score = max(1, 5 - len(broken_links) * 2)
        notes.append(f"G4 Grounding: Missing local targets: {', '.join(broken_links[:3])}.")
    scores["G4"] = g4_score

    # G5: Honesty (fabricated social proof)
    fake_stats = re.findall(r"\b(?:99\.9%|trusted by \d+|10,000\+ developers|\+90% productivity)\b", content, re.IGNORECASE)
    g5_score = 5
    if fake_stats:
        g5_score = 2
        notes.append(f"G5 Honesty: Unsubstantiated marketing metrics found: {fake_stats}.")
    scores["G5"] = g5_score

    # G6: Governance (status, license references)
    g6_score = 5
    if "LICENSE" not in content and "license" not in content.lower():
        g6_score = 3
        notes.append("G6 Governance: No clear license reference detected.")
    scores["G6"] = g6_score

    return scores, notes


def render_terminal_preview(content):
    """Format markdown content for clean terminal viewing."""
    lines = content.splitlines()
    output = []
    in_code_block = False

    for line in lines:
        # Code fence
        if line.startswith("```"):
            in_code_block = not in_code_block
            output.append(f"{DIM}{line}{RESET}")
            continue

        if in_code_block:
            output.append(f"  {CYAN}{line}{RESET}")
            continue

        # Headings
        if line.startswith("# "):
            output.append(f"\n{BOLD}{MAGENTA}{'=' * 60}\n# {line[2:]}\n{'=' * 60}{RESET}")
        elif line.startswith("## "):
            output.append(f"\n{BOLD}{CYAN}## {line[3:]}\n{'-' * 40}{RESET}")
        elif line.startswith("### "):
            output.append(f"\n{BOLD}{GREEN}### {line[4:]}{RESET}")
        elif line.startswith("#### "):
            output.append(f"\n{BOLD}{YELLOW}#### {line[5:]}{RESET}")
        elif line.startswith("> "):
            output.append(f"  {DIM}│ {line[2:]}{RESET}")
        elif line.startswith("- ") or line.startswith("* "):
            output.append(f"  {CYAN}•{RESET} {line[2:]}")
        elif re.match(r"^\d+\.\s", line):
            output.append(f"  {YELLOW}{line}{RESET}")
        elif line.startswith("|") and line.endswith("|"):
            output.append(f"{DIM}{line}{RESET}")
        elif line.strip() == "---":
            output.append(f"{DIM}{'─' * 60}{RESET}")
        else:
            output.append(line)

    return "\n".join(output)


def print_scorecard(scores, notes):
    """Print the 6-gate audit scorecard banner."""
    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}well-document · Pre-Emit Audit Scorecard{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}")

    all_pass = True
    score_line = []
    for gate in ["G1", "G2", "G3", "G4", "G5", "G6"]:
        val = scores.get(gate, 5)
        if val >= 4:
            color = GREEN
        elif val == 3:
            color = YELLOW
            all_pass = False
        else:
            color = RED
            all_pass = False
        score_line.append(f"{BOLD}{gate}:{color}{val}{RESET}")

    status_str = f"{GREEN}PASS{RESET}" if all_pass else f"{RED}FAIL (Revision Needed){RESET}"
    print("  " + "  ".join(score_line) + f"  ·  STATUS: {status_str}")

    if notes:
        print(f"\n{DIM}Audit Findings:{RESET}")
        for n in notes:
            print(f"  {YELLOW}!{RESET} {n}")
    else:
        print(f"\n  {GREEN}✓ Zero anti-slop violations or ungrounded targets detected.{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Terminal Markdown Preview & Pre-Emit Inspector")
    parser.add_argument("file", nargs="?", default="README.md", help="Markdown file to preview (default: README.md)")
    parser.add_argument("--score-only", action="store_true", help="Print only the audit scorecard")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI color output")
    parser.add_argument("--diff", action="store_true", help="Show diff against git HEAD")
    args = parser.parse_args()

    if args.no_color or not sys.stdout.isatty():
        disable_colors()

    if not os.path.isfile(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    scores, notes = evaluate_document(content, args.file)

    if args.diff:
        try:
            import subprocess
            head_content = subprocess.check_output(["git", "show", f"HEAD:{args.file}"], text=True)
            diff = difflib.unified_diff(
                head_content.splitlines(),
                content.splitlines(),
                fromfile=f"HEAD:{args.file}",
                tofile=args.file,
                lineterm=""
            )
            print("\n".join(diff))
            return 0
        except Exception as e:
            print(f"Unable to compute git diff: {e}", file=sys.stderr)
            return 1

    if args.score_only:
        print_scorecard(scores, notes)
        return 0 if all(v >= 3 for v in scores.values()) else 1

    # Render formatted markdown preview
    print(render_terminal_preview(content))
    print_scorecard(scores, notes)

    return 0 if all(v >= 3 for v in scores.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
