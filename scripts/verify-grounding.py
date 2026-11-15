#!/usr/bin/env python3
"""
verify-grounding.py - Verify Codebase Grounding & Markdown Link Integrity
Checks that relative links in markdown files physically resolve to files on disk.
Zero external dependencies.
"""

import os
import re
import subprocess
import sys


def get_staged_or_all_files():
    """Detect files to verify: arguments -> staged markdown files -> all markdown files."""
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

    all_md = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        for f in files:
            if f.endswith(".md"):
                all_md.append(os.path.normpath(os.path.join(root, f)))
    return sorted(all_md)


def check_markdown_links(file_path):
    """Scan markdown file for ungrounded relative links."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Unable to read file: {e}"]

    # Strip code blocks and inline code
    content = re.sub(r"```[\s\S]*?```", "", content)
    content = re.sub(r"`[^`]*`", "", content)

    # Match markdown links: [text](target)
    # Ignore absolute URLs (http, https, mailto) and pure in-page anchors (#)
    pattern = r"\[.*?\]\((?!https?://|mailto:)(.*?)\)"
    matches = re.findall(pattern, content)

    broken = []
    file_dir = os.path.dirname(os.path.abspath(file_path))

    for raw_link in matches:
        link = raw_link.strip()
        if not link or link.startswith("#"):
            continue

        # Strip anchor fragment (#section) and query string (?raw=true)
        link_target = link.split("#")[0].split("?")[0].strip()
        if not link_target:
            continue

        resolved = os.path.normpath(os.path.join(file_dir, link_target))
        if not os.path.exists(resolved):
            broken.append(f"{file_path}: broken link '{link_target}' (resolved: '{resolved}')")

    return broken


def main():
    files = get_staged_or_all_files()
    if not files:
        print("verify-grounding: No markdown files found to verify.")
        return 0

    total_broken = []
    for f in files:
        issues = check_markdown_links(f)
        total_broken.extend(issues)

    if total_broken:
        print("verify-grounding: FAILED. Found broken or ungrounded links:\n", file=sys.stderr)
        for issue in total_broken:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print(f"verify-grounding: PASSED. Checked {len(files)} markdown file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
