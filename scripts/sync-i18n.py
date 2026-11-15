#!/usr/bin/env python3
"""
sync-i18n.py - Multi-Lingual Documentation Synchronizer & Anti-Slop Auditor
Scaffolds structured translation templates from source markdown and audits
existing translations against structural drift and machine translation slop.
Zero external dependencies.
"""

import argparse
import os
import re
import sys

# Multilingual forbidden buzzword dictionary
MULTILINGUAL_SLOP = {
    "en": [
        r"\bseamlessly\b",
        r"\bblazingly fast\b",
        r"\bcutting-edge\b",
        r"\brevolutionary\b",
        r"\bcomprehensive and robust\b",
        r"\beffortlessly\b",
    ],
    "tr": [
        r"\bkesintisiz biçimde\b",
        r"\bışık hızında\b",
        r"\bson teknoloji\b",
        r"\bdevrim niteliğinde\b",
        r"\bkapsamlı ve sağlam\b",
        r"\bzahmetsizce\b",
    ],
    "de": [
        r"\bnahtlos\b",
        r"\bblitzschnell\b",
        r"\bspitzentechnologie\b",
        r"\brevolutionär\b",
        r"\bmühelos\b",
    ],
    "fr": [
        r"\bde manière transparente\b",
        r"\bultra-rapide\b",
        r"\brévolutionnaire\b",
        r"\bsans effort\b",
    ],
    "es": [
        r"\bperfectamente integrado\b",
        r"\bultrarrápido\b",
        r"\bvanguardista\b",
        r"\brevolucionario\b",
        r"\bsin esfuerzo\b",
    ],
}

EXCLUSIONS = [
    r"zero buzzword",
    r"strips meaningless",
    r"banned buzzwords",
    r"catalog of ai-slop",
    r"forbidden",
    r"anti-pattern",
    r"yasaklı",
]


def should_skip_line(line):
    lower = line.lower()
    return any(re.search(pat, lower) for pat in EXCLUSIONS)


def extract_headings(content):
    """Extract list of (level, title) tuples from markdown content."""
    clean = re.sub(r"```[\s\S]*?```", "", content)
    headings = []
    for line in clean.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if match:
            headings.append((len(match.group(1)), match.group(2).strip()))
    return headings


def extract_code_blocks(content):
    """Extract list of code blocks (language, body) from markdown."""
    return re.findall(r"```([a-zA-Z0-9_\-]+)?\n([\s\S]*?)```", content)


def audit_translation(source_path, target_path, lang="en"):
    """Audit a translated markdown file against source document."""
    issues = []

    if not os.path.isfile(source_path):
        return [f"Source file not found: {source_path}"]
    if not os.path.isfile(target_path):
        return [f"Target translation file not found: {target_path}"]

    with open(source_path, "r", encoding="utf-8") as f:
        src_content = f.read()
    with open(target_path, "r", encoding="utf-8") as f:
        tgt_content = f.read()

    # 1. Heading structure alignment
    src_headings = extract_headings(src_content)
    tgt_headings = extract_headings(tgt_content)

    if len(src_headings) != len(tgt_headings):
        issues.append(
            f"Heading count mismatch: source has {len(src_headings)} headings, target has {len(tgt_headings)}."
        )
    else:
        for idx, ((s_lvl, _), (t_lvl, _)) in enumerate(zip(src_headings, tgt_headings)):
            if s_lvl != t_lvl:
                issues.append(f"Heading level mismatch at position {idx + 1}: expected H{s_lvl}, got H{t_lvl}.")

    # 2. Code block count and verbatim preservation
    src_code = extract_code_blocks(src_content)
    tgt_code = extract_code_blocks(tgt_content)

    if len(src_code) != len(tgt_code):
        issues.append(
            f"Code block count mismatch: source has {len(src_code)} code blocks, target has {len(tgt_code)}."
        )
    else:
        for idx, ((s_lang, s_body), (t_lang, t_body)) in enumerate(zip(src_code, tgt_code)):
            if s_lang != t_lang:
                issues.append(
                    f"Code block language tag mismatch at block {idx + 1}: expected '{s_lang}', got '{t_lang}'."
                )
            if s_body.strip() != t_body.strip():
                issues.append(
                    f"Code block content altered at block {idx + 1}. Code and terminal commands must remain verbatim."
                )

    # 3. Machine Translation Slop Check
    buzzwords = MULTILINGUAL_SLOP.get(lang, []) + MULTILINGUAL_SLOP["en"]
    tgt_lines = tgt_content.splitlines()
    in_code = False
    for idx, line in enumerate(tgt_lines, start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or should_skip_line(line):
            continue
        for pat in buzzwords:
            matches = re.findall(pat, line, re.IGNORECASE)
            if matches:
                issues.append(f"Line {idx}: Forbidden translation buzzword detected: '{matches[0]}'.")

    # 4. Long dash (em-dash) detection
    for idx, line in enumerate(tgt_lines, start=1):
        if should_skip_line(line):
            continue
        if "—" in line:
            issues.append(f"Line {idx}: Forbidden long dash (em-dash '—') detected in translated text.")

    # 5. Link grounding in target
    clean_tgt = re.sub(r"```[\s\S]*?```", "", tgt_content)
    clean_tgt = re.sub(r"`[^`]*`", "", clean_tgt)
    links = re.findall(r"\[.*?\]\((?!https?://|mailto:)(.*?)\)", clean_tgt)
    base_dir = os.path.dirname(os.path.abspath(target_path))

    for raw_link in links:
        target = raw_link.split("#")[0].split("?")[0].strip()
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(base_dir, target))
        if not os.path.exists(resolved):
            issues.append(f"Broken relative link in translation: '{target}' (resolved: '{resolved}').")

    return issues


def adjust_relative_link(match, rel_prefix):
    """Rewrite relative markdown link targets with relative prefix."""
    text = match.group(1)
    target = match.group(2)
    if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:") or target.startswith("#"):
        return f"[{text}]({target})"

    # Handle anchor suffix
    parts = target.split("#", 1)
    path_part = parts[0]
    anchor = f"#{parts[1]}" if len(parts) > 1 else ""

    if not path_part:
        return f"[{text}]({target})"

    new_path = os.path.normpath(os.path.join(rel_prefix, path_part))
    return f"[{text}]({new_path}{anchor})"


def adjust_img_src(match, rel_prefix):
    tag = match.group(0)
    src_match = re.search(r'src=["\']([^"\']+)["\']', tag)
    if not src_match:
        return tag
    src = src_match.group(1)
    if src.startswith("http://") or src.startswith("https://"):
        return tag
    new_src = os.path.normpath(os.path.join(rel_prefix, src))
    return tag.replace(src, new_src)


def scaffold_template(source_path, target_path, lang="tr"):
    """Scaffold a translation template maintaining verbatim code blocks and structure."""
    if not os.path.isfile(source_path):
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        return 1

    with open(source_path, "r", encoding="utf-8") as f:
        src_content = f.read()

    lines = src_content.splitlines()
    scaffolded = []
    in_code_block = False

    source_dir = os.path.dirname(os.path.abspath(source_path))
    target_dir = os.path.dirname(os.path.abspath(target_path))
    rel_prefix = os.path.relpath(source_dir, target_dir)

    # Backlink header
    backlink_rel = os.path.relpath(source_path, target_dir)
    scaffolded.append(f"[← Read Original in English]({backlink_rel})\n")

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            scaffolded.append(line)
            continue

        if in_code_block:
            # Code block lines must remain 100% verbatim
            scaffolded.append(line)
            continue

        # If target is in a subfolder, adjust relative links
        if rel_prefix != ".":
            # Adjust [text](link) and [![badge](img)](link)
            line = re.sub(
                r"\[(!?\[.*?\]\(.*?\)|[^\]]+)\]\(([^)]+)\)",
                lambda m: adjust_relative_link(m, rel_prefix),
                line
            )
            # Adjust <img src="...">
            line = re.sub(
                r"<img\s+[^>]*src=[\"'][^\"']+[\"'][^>]*>",
                lambda m: adjust_img_src(m, rel_prefix),
                line
            )

        scaffolded.append(line)

    if target_dir:
        os.makedirs(target_dir, exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(scaffolded) + "\n")

    print(f"sync-i18n: Scaffolded translation template at '{target_path}'.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Multi-Lingual Documentation Synchronizer & Slop Auditor")
    parser.add_argument("--source", "-s", default="README.md", help="Path to source documentation (default: README.md)")
    parser.add_argument("--target", "-t", help="Path to target translation file")
    parser.add_argument("--lang", "-l", default="en", help="Language code (en, tr, de, fr, es)")
    parser.add_argument("--audit", action="store_true", help="Audit existing translation file against source")
    parser.add_argument("--init", help="Scaffold a new translation template for the given language code")
    args = parser.parse_args()

    if args.init:
        lang_code = args.init.lower()
        target = args.target or f"docs/translations/README.{lang_code}.md"
        return scaffold_template(args.source, target, lang=lang_code)

    if args.audit:
        if not args.target:
            print("Error: --target path required for --audit", file=sys.stderr)
            return 1
        issues = audit_translation(args.source, args.target, lang=args.lang)
        if issues:
            print(f"sync-i18n: FAILED. Found {len(issues)} translation issue(s):\n", file=sys.stderr)
            for iss in issues:
                print(f"  - {iss}", file=sys.stderr)
            return 1
        print(f"sync-i18n: PASSED. '{args.target}' is structurally aligned and free of translation slop.")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
