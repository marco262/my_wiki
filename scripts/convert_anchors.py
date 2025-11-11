import html
import re
from pathlib import Path

PATHS = [
    r"..\data\dnd\general\rules-glossary.md",
    r"..\data\dnd\general\playing-the-game.md",
    r"..\data\dnd\advancement\creating-a-character.md",
]

# Anchors
# REG = r'<a[^>]*href\s*=\s*["\']#([^"\']*)["\'][^>]*>(.*?)</a>'
# FORMAT_STRING = '[{label}](#{label})'
# FORMAT_STRING2 = '[{label}](#{slug})'

# Glossary links
# REG = r'<a class="tooltip-hover (?:action|rule|condition)-tooltip" href="/sources/dnd/free-rules/rules-glossary#(.*?)" data-tooltip-href=".*?">(.*?)</a>'
# FORMAT_STRING = '[[glossary:{label}]]'
# FORMAT_STRING2 = '[[glossary:{label}|{slug}]]'

# Playing the Game links
# REG = r'\<a href\=\"\/sources\/dnd\/br\-2024\/playing\-the\-game\#(.*?)\"\>(.*?)\<\/a\>'
# FORMAT_STRING = '[[[general:Playing the Game#{label}]]]'
# FORMAT_STRING2 = '[[[general:Playing the Game#{slug}|{label}]]]'

# Creating a Character links
# REG = r'\<a href\=\"\/sources\/dnd\/br\-2024\/creating\-a\-character\#(.*?)\"\>(.*?)\<\/a\>'
# FORMAT_STRING = '[[[general:Creating a Character#{label}]]]'
# FORMAT_STRING2 = '[[[general:Creating a Character#{slug}|{label}]]]'

# Equipment links
# REG = r'\<a href\=\"\/sources\/dnd\/br\-2024\/equipment\#(.*?)\"(?: data-content-chunk-id=".*?")?\>(.*?)\<\/a\>'
# FORMAT_STRING = '[[[general:Equipment#{label}]]]'
# FORMAT_STRING2 = '[[[general:Equipment#{slug}|{label}]]]'

# Equipment links
REG = r'\<a href\=\"\/sources\/dnd\/br\-2024\/dms\-toolbox\#(.*?)\"(?: data-content-chunk-id=".*?")\>(.*?)\<\/a\>'
FORMAT_STRING = '[[[general:Equipment#{label}]]]'
FORMAT_STRING2 = '[[[general:Equipment#{slug}|{label}]]]'


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
    anchor_re = re.compile(REG, re.IGNORECASE | re.DOTALL)

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

        if label == slug:
            r = FORMAT_STRING.format(label=label)
        else:
            r = FORMAT_STRING2.format(label=label, slug=slug)

        print(f"{m.group(0)} -> {r}")
        return r

    new_text, n = anchor_re.subn(repl, s)
    return new_text, n


def process_file(path: str):
    print(f"Processing {path}...")
    filepath = Path(path)
    if not filepath.exists():
        print(f"File not found: {filepath}")
        raise SystemExit(1)

    text = filepath.read_text(encoding="utf-8")
    new_text, count = convert_anchors_in_text(text)

    if count == 0:
        print("No same-page <a href=\"#...\">...</a> anchors found to convert.")
        return

    filepath.write_text(new_text, encoding="utf-8")


def main():
    for path in PATHS:
        process_file(path)


if __name__ == '__main__':
    main()
