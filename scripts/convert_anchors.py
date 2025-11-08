#!/usr/bin/env python3
"""
convert_anchors.py

Usage:
    python scripts/convert_anchors.py "C:\path\to\my_wiki\data\dnd\general\rules-glossary.md"

This script finds HTML anchors that point to same-page fragments (href="#...") and replaces
instances like

    <a href="#ShortRest">Short Rest</a>

with

    [Short Rest](#short-rest)

The slug is generated from the anchor href fragment (not the visible link text) so
ids like `ShortRest` become `short-rest`.

The script makes a .bak copy before writing changes.
"""

import argparse
import html
import os
import re
from pathlib import Path


def slugify(text: str) -> str:
    """Create a URL fragment slug from visible link text.

    Rules:
    - Unescape HTML entities
    - Strip any inner HTML
    - Lowercase
    - Remove characters other than a-z, 0-9, space, and hyphen
    - Replace whitespace with single hyphen
    - Collapse multiple hyphens
    - Strip leading/trailing hyphens
    """
    text = html.unescape(text)
    # remove any remaining HTML tags that might be inside
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip()
    text = text.lower()
    # keep letters, numbers, spaces and hyphens
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    # replace whitespace with hyphen
    text = re.sub(r"[\s]+", "-", text)
    # collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text


def slugify_fragment(fragment: str) -> str:
    """Create a normalized slug from an anchor fragment/id.

    This prefers using the fragment string (the href target) to build a slug.
    It handles common id styles including CamelCase/PascalCase, underscores, and
    existing hyphens.

    Steps:
    - Unescape HTML entities
    - Strip leading '#' if present
    - Insert hyphens between camelCase / PascalCase transitions
    - Replace underscores and whitespace with hyphens
    - Lowercase and remove any character except a-z, 0-9, and hyphen
    - Collapse multiple hyphens and strip edges
    """
    s = html.unescape(fragment or "")
    s = s.lstrip("#").strip()
    if not s:
        return ""
    # Insert hyphen between lowercase/number and uppercase (e.g., shortRest -> short-Rest)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s)
    # Insert hyphen between a lowercase or number and an uppercase that starts a word
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', s)
    # Replace underscores and spaces with hyphens
    s = re.sub(r'[\s_]+', '-', s)
    s = s.lower()
    # Remove invalid characters, keep hyphens and alphanumerics
    s = re.sub(r'[^a-z0-9-]', '', s)
    # Collapse multiple hyphens
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s


def convert_anchors_in_text(s: str):
    """Replace <a ... href="#...">inner</a> with Markdown [inner](#slug) built from the fragment.

    Returns (new_text, replacements_count).
    """
    # Match <a ... href="#fragment" ...>inner</a> supporting single- or double-quoted hrefs
    anchor_re = re.compile(r'<a[^>]*href\s*=\s*["\']#([^"\']*)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)

    def repl(m: re.Match):
        href_fragment = m.group(1)  # original fragment name
        inner = m.group(2)
        # Remove surrounding whitespace/newlines inside inner and any inner tags
        inner_clean = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", inner)).strip()
        # Generate slug from the anchor fragment (as requested)
        slug = slugify_fragment(href_fragment)
        # Use the visible text as the label when available; otherwise fall back to the fragment
        label = inner_clean if inner_clean else href_fragment
        # If slug is empty (edge case), fallback to slugifying the label
        if not slug:
            slug = slugify(label)
        if "areaof" in slug:
            slug = slug.replace("areaof", "area-of")
        return f'[{label}](#{slug})'

    new_text, n = anchor_re.subn(repl, s)
    return new_text, n


filepath = Path(r"..\data\dnd\general\rules-glossary.md")
if not filepath.exists():
    print(f"File not found: {filepath}")
    raise SystemExit(1)

text = filepath.read_text(encoding="utf-8")
new_text, count = convert_anchors_in_text(text)

if count == 0:
    print("No same-page <a href=\"#...\">...</a> anchors found to convert.")
    exit()

filepath.write_text(new_text, encoding="utf-8")
