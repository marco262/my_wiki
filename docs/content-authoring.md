# Content Authoring

This repo is mostly content-driven. Pages live under `data/`, route through namespace endpoints, and are rendered by the custom Markdown parser in `src/common/markdown_parser.py`.

Use this guide when adding or editing wiki pages, campaign notes, GM notes, visual aid links, sound links, includes, and other custom Markdown features.

## Public vs GM Content

Most namespaces under `data/` can have both public pages and GM-only pages.

- `data/<namespace>/...` is public/player-facing by default.
- `data/<namespace>/gm_notes/...` is GM-facing and generally password-protected.
- Do not move spoilers, hidden mechanics, private prep, stat block details, or unrevealed plot information from `gm_notes` into adjacent public pages.
- If the user says "public-facing," edit the file outside `gm_notes`.
- If the user says "GM notes," "gm_notes," or "private notes," edit the file inside `gm_notes`.

Examples:

```text
data/class_1a/adventure-options.md              public player-facing page
data/class_1a/gm_notes/adventure-options.md     GM-facing private page
```

## File Names and URLs

Page names are normalized by `title_to_page_name()`:

- lowercased
- apostrophes removed
- non-word characters converted to hyphens
- leading/trailing hyphens stripped

Examples:

```text
Adventure Options      -> adventure-options.md
Shemshime's Rhyme      -> shemshimes-rhyme.md
The Forge of Fury      -> the-forge-of-fury.md
```

Namespace routes usually resolve pages like this:

```text
/<namespace>/<page>              -> data/<namespace>/<page>.md
/<namespace>/<category>/<page>   -> data/<namespace>/<category>/<page>.md
/<namespace>/gm_notes/<page>     -> data/<namespace>/gm_notes/<page>.md
```

The active namespace list is in `src/__init__.py` as `MODULE_NAMES`.

## Front Matter

Markdown files can use metadata front matter. The most common key is `toc`.

```yaml
---
toc: false
---
```

Use `toc: false` for short pages, player handouts, or pages whose headings should not produce a table of contents.

Preserve existing front matter unless the user asks to change it.

## Standard Markdown

The parser is based on `markdown2` and supports:

- heading IDs
- tables
- wiki tables
- table of contents generation
- strikethrough
- task lists
- Markdown inside HTML
- metadata/front matter

Prefer normal Markdown where it works. Use custom syntax only for site-specific behavior.

## Same-Folder Links

A link with empty parentheses points to a same-folder page with the same display text:

```md
[Notebook]()
```

This becomes a link to `Notebook`, resolved by the current namespace/directory route.

A link with `#` points to a same-page heading anchor generated from the label:

```md
[Important NPCs](#)
```

This becomes:

```md
[Important NPCs](#important-npcs)
```

## Wiki Links

Triple-bracket links create namespace-aware links:

```md
[[[class:Wizard]]]
[[[spell:Fireball]]]
[[[race:Elf#Traits|Elf Traits]]]
```

General shape:

```md
[[[category:Page Name#Heading|Display Text]]]
```

Rules:

- `category:` is optional.
- `#Heading` is optional.
- `|Display Text` is optional.
- Slashes in page names are converted to hyphens.
- The current namespace is prepended automatically.

Example in the `dnd` namespace:

```md
[[[spell:Fireball]]]
```

links to:

```text
/dnd/spell/Fireball
```

If the target file is missing, the parser marks the link as broken.

## Visual Aid Links

Use `^` links for images that should be clickable as visual aids and show hover previews:

```md
[Museum Exterior](^class_1a/museum-exterior.png)
```

If the path is not an absolute URL, it is treated as relative to:

```text
/media/img/visual_aids/
```

So this:

```md
[Class Portrait](^class_1a/Class_1A.png)
```

points to:

```text
/media/img/visual_aids/class_1a/Class_1A.png
```

Use `@` links for popup image links:

```md
[Handout](@handouts/some-image.png)
```

Use normal Markdown links for ordinary navigation.

## Sound and Visual Aid Commands

Use `$` links to create controls for the visual aid backend:

```md
[Pre-session music]($load|music|arr/BGM_Event_Crystal.mp3)
[Pause All]($pause|all)
```

Common action pattern:

```text
$action|target|path
```

These become clickable spans with `visual-aid-link` behavior. The browser-side code in `static/js/common/visual_aid_backend.js` sends the command to the server, and the visual aid page receives updates over websockets.

Keep audio paths aligned with files under:

```text
media/audio/
```

## Includes

Use includes to embed templates or Markdown files.

Template include:

```md
[[include dnd/monster-sheet.tpl]]
name = Fey Spirit
width = 500px
actions = !!!
***Multiattack.*** The creature makes two attacks.
!!!
[[/include]]
```

Markdown include:

```md
[[include class_1a/gm_notes/some-shared-note.md]]
```

Include argument behavior:

- `key = value` passes a plain string.
- `key = !markdown text` parses a single line as Markdown.
- `key = !!! ... !!!` parses a multiline block as Markdown.
- `file = path/to/file.toml` loads TOML from `data/` and passes its keys as template args.
- `glob = media/path/*` expands matching media files, useful for galleries.

## Breadcrumbs

Use breadcrumbs at the top of pages that need a backlink:

```md
[[breadcrumb /class_1a/|Class 1A]]
```

This renders a left-arrow backlink.

## Content Blocks

The parser supports a few custom block markers:

```md
[[sidebar]]
Sidebar content
[[/sidebar]]

[[errata]]
Errata content
[[/errata]]

[[homebrew]]
Homebrew note
[[/homebrew]]
```

These become styled HTML blocks.

Use accordions for collapsible sections:

```md
[[accordion Optional Details]]
Hidden content.
[[/accordion]]
```

Use `[[clear-float]]` as a layout escape hatch after right-floated content, such as a floated image, sidebar, or monster stat block. It renders:

```html
<div class="clear-float"></div>
```

The CSS applies `clear: right`, which forces following content to start below any active right-floated element instead of wrapping beside it.

Use it when a later heading, paragraph, table, or section is visually pulled up beside a right-floated element and should instead begin underneath that element. Do not use it as ordinary spacing; it is only for fixing float wrapping.

## Tooltips and Glossary Links

Use equipment/reference tooltips:

```md
[[tooltip:Leather Armor]]
[[tooltip:Longsword|the blade]]
```

Use D&D rules glossary tooltips:

```md
[[glossary:Unarmed Strike]]
[[glossary:Armor Training|armor training]]
```

Broken tooltip keys are rendered as broken tooltip elements and logged.

## Magic Item Tracker

Use the magic item tracker block for campaign magic item lists:

```md
[[magic-item-tracker]]
* Dagger of Returning -- Minor Uncommon
* Clockwork Amulet -- Minor Common
[[/magic-item-tracker]]
```

The parser leaves the item list in place and appends a generated tracker table plus a magic item reference link.

## NPC Blocks

Use `[[npc ...]]` to generate an NPC stat block:

```md
[[npc cr=2|race=Human|role=Scout]]
```

Arguments are pipe-delimited `key=value` pairs. The parser calls `src.dnd5e.npc_generator.create_npc()` and renders `views/dnd/npc-sheet.tpl`.

Use this for generated quick NPCs. For important custom monsters or NPCs, a hand-authored stat block or linked source may be clearer.

## GM Note Inserts

`[[gm_notes Name]]` creates a collapsible GM-notes placeholder in a public page:

```md
[[gm_notes Secret Door]]
```

This renders a `<details class="gm-notes">` block with the generated ID for `Name`:

```html
<details class="gm-notes" id="secret-door">
    <summary>GM Notes for Secret Door</summary>
</details>
```

The placeholder is only the visible shell. To make it load content on click, the namespace needs three pieces:

1. An insert file at:

   ```text
   data/<namespace>/gm_notes/inserts/<generated-id>.md
   ```

   For `[[gm_notes Secret Door]]`, the expected file is:

   ```text
   data/<namespace>/gm_notes/inserts/secret-door.md
   ```

2. A protected namespace endpoint like:

   ```python
   @app.get("gm_notes/insert/<name>")
   @auth_basic(gm_notes_auth_check)
   def gm_notes_insert(name):
       return md_page(name, "<namespace>", directory="gm_notes/inserts", load_template=False)
   ```

3. Page JavaScript that initializes the insert loader with the namespace:

   ```html
   <script type="module">
       import {init_gm_notes_inserts} from "/static/js/common/gm_notes.js";
       init_gm_notes_inserts("<namespace>");
   </script>
   ```

When the user expands the `<details>` block for the first time, `static/js/common/gm_notes.js` fetches:

```text
/<namespace>/gm_notes/insert/<generated-id>
```

The endpoint is protected with GM basic auth. If the user is not authenticated, the expanded block shows a sign-in message.

This is different from directly linking to a page inside `gm_notes`; it is inline public-page markup that lazy-loads a private GM-only insert.

## Bibliography

Use bibliography blocks with `[((bibcite name))]` references:

```md
Some claim.[((bibcite source1))]

[[bibliography]]
: source1 : Source description or link
[[/bibliography]]
```

The parser converts citations to numbered links and renders an ordered bibliography.

## Media Files

Media requests go through `/media/<path>`.

The server first checks local files under `media/`. If no local file exists and `media bucket` is configured, it redirects to the configured Google Cloud Storage bucket.

Do not assume production has every media file locally checked out.

Common locations:

```text
media/img/visual_aids/<namespace>/
media/img/handouts/<namespace>/
media/img/fanart/<namespace>/
media/audio/<namespace>/
media/audio/requests/
```

## Public Page Checklist

Before editing or creating a public page:

- Confirm the file is outside `gm_notes`.
- Keep spoilers and mechanics out unless explicitly public.
- Use player-facing language.
- Prefer concise hooks, summaries, and links.
- Preserve existing front matter.

## GM Page Checklist

Before editing or creating a GM page:

- Confirm the file is inside `gm_notes`.
- Include mechanics, hidden information, stat links, and prep notes as needed.
- Link to source material instead of copying long source text.
- Put reusable NPC, monster, hazard, and location details in dedicated sections when the page is complex.
- For adventure notes, use or consult `docs/adventure-note-template.md`.

## Validation

Useful checks after content changes:

```bash
python -m unittest tests.functional.test_md_pages
python -m unittest tests.unit.test_markdown_parser
```

The functional Markdown test attempts to render every Markdown file under `data/`, which is useful for catching broken includes or malformed custom syntax.
