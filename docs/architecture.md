# Project Architecture

`my_wiki` is a personal Bottle-based wiki and table tool server. It serves Markdown/TOML campaign and rules content from `data/`, renders specialized Bottle templates from `views/`, hosts local or bucket-backed media from `media/`, and provides a few live table tools such as visual aids, soundboards, calendars, Tarokka controls, D&D spell and magic-item filters, and monster/stat-block pages.

## Top-Level Layout

| Path                 | Purpose                                                                                                                                                                   |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `main.py`            | CLI entry point. Creates `src.server.Server` and restarts through a watchdog-style loop unless disabled.                                                                  |
| `src/`               | Python application code. Contains the server bootstrap, shared utilities, Markdown parsing, namespace route modules, D&D data utilities, calendars, generators, and APIs. |
| `data/`              | Content store. Namespaces under this folder map to mounted URL namespaces such as `/dnd/` or `/class_1a/`.                                                                |
| `views/`             | Bottle templates used for page shells, tools, stat blocks, filters, calendars, and namespace-specific interfaces.                                                         |
| `static/`            | CSS and JavaScript served directly under `/static/`. Includes visual aid, soundboard, calendar, search/filter, and sheet UI behavior.                                     |
| `media/`             | Images, handouts, visual aids, audio, Tarokka images, and other table media. Can be served locally or redirected to a Google Cloud Storage bucket.                        |
| `scripts/`           | One-off and maintenance scripts for parsing D&D data, checking data consistency, downloading/processing media, and table utilities.                                       |
| `tests/`             | Unit and functional tests for Markdown parsing, utility behavior, magic-item tracking, and bulk Markdown page rendering.                                                  |
| `terraform/`         | Google Cloud infrastructure definitions, including VM and bucket resources.                                                                                               |
| `.github/workflows/` | GitHub Actions automation. Currently pings the live server's `/load_changes` endpoint after pushes.                                                                       |
| `docs/`              | Repository documentation. This file is the first repo architecture overview.                                                                                              |
| `AGENTS.md`          | Persistent guidance for coding agents, especially around public vs GM-only content boundaries.                                                                            |

## Runtime Flow

1. `main.py` parses `--debug` and `--disable-watchdog`.
2. `main.py` constructs `src.server.Server`.
3. `Server` takes an interprocess lock using `server.lock` to prevent multiple server instances.
4. `Server` loads `config.ini` through `src.common.utils.load_config()`. If missing, it copies `config.ini.dist`.
5. `Server` creates a `bottle.Bottle()` app and calls `src.load_wsgi_endpoints(app, cfg)`.
6. `src.__init__.load_wsgi_endpoints()` loads each namespace module listed in `MODULE_NAMES`.
7. `common` routes are installed directly on the root app. Other namespace apps are mounted under `/<namespace>/`.
8. Any namespace with an `api.py` module is mounted under `/api/<namespace>/`.
9. The app runs with `GeventWebSocketServer`, enabling the visual aid and other websocket tools.

The app is designed around a single long-running Bottle process. Deployment can be direct Python, tmux, Docker, or a VM behind Nginx.

## Namespace Routing

The active namespace list lives in `src/__init__.py` as `MODULE_NAMES`. Treat that file, not this document, as the source of truth for which namespaces are currently enabled. Namespaces can be added or removed over time without changing the overall architecture.

Each namespace normally has:

- `src/<namespace>/endpoints.py` for routes.
- `data/<namespace>/` for Markdown/TOML/JSON content.
- Optional `views/<namespace>/` templates.
- Optional `static/js/<namespace>/` and `static/css/<namespace>.css` assets.
- Optional `media/.../<namespace>/` visual aids or audio.

Most campaign namespaces follow a simple route pattern:

- `/<namespace>/` or `/<namespace>/home` renders the namespace home page.
- `/<namespace>/<name>` renders `data/<namespace>/<page-name>.md`.
- `/<namespace>/<category>/<name>` renders a categorized page when implemented.
- `/<namespace>/gm_notes/<name>` renders `data/<namespace>/gm_notes/<page-name>.md` behind GM basic auth.

Rules namespaces, such as `dnd` and `dnd5e`, tend to be more tool-heavy than campaign namespaces. They can expose category pages, spells, magic items, monsters, filters, search, generators, and optional API endpoints.

## Content Model

The main content store is `data/`. It contains both rules references and campaign notes.

Important conventions:

- Markdown files are ordinary pages and are rendered through `src.common.utils.md_page()`.
- TOML files are structured data pages, especially for D&D spells, magic items, and monsters.
- JSON files are used for character data, saved tool state, readings, and other structured content.
- The page name in the URL is normalized with `title_to_page_name()`, which lowercases, strips punctuation, and uses hyphens.
- A `gm_notes` folder inside any namespace is GM-facing and generally password-protected.
- Files adjacent to `gm_notes` are public/player-facing unless explicitly protected by a route.

Examples:

- `/class_1a/adventure-options` maps to `data/class_1a/adventure-options.md`.
- `/class_1a/gm_notes/adventure-options` maps to `data/class_1a/gm_notes/adventure-options.md` and requires GM auth.
- `/dnd/spell/fireball` loads structured spell data from `data/dnd/spell/fireball.toml`.
- `/dnd/equipment/magic-item/...` loads structured magic item data from `data/dnd/equipment/magic-items/`.

## Markdown Rendering

Markdown rendering is centralized in `src/common/markdown_parser.py`.

`MarkdownParser` wraps `markdown2` with extras for metadata, generated header IDs, tables, task lists, table of contents, and Markdown-in-HTML. It also performs custom pre-processing and post-processing.

Notable custom syntax:

- `[[[category:Page Name]]]` creates namespace-aware wiki links.
- `[[[category:Page Name#Heading|Label]]]` creates wiki links with anchors and display text.
- `[Text]()` links to a same-folder page named `Text`.
- `[Heading](#)` links to the generated anchor for `Heading`.
- `[Name](^path/to/image.png)` creates a visual-aid link and hover preview.
- `[Name](@path/to/image.png)` creates a popup image link.
- `[Sound]($load|music|file.mp3)` and similar `$...` links create visual-aid backend controls.
- `[[include template.tpl]]...[[/include]]` includes Bottle templates with arguments.
- `[[include path/to/file.md]]` includes Markdown content from `data/`.
- `[[breadcrumb /path/|Label]]` inserts a breadcrumb link.
- `[[magic-item-tracker]]...[[/magic-item-tracker]]` expands campaign magic item lists into tracker tables.
- `[[accordion Title]]...[[/accordion]]` creates collapsible sections.
- `[[tooltip:Name]]` and `[[glossary:Name]]` create D&D reference tooltips.
- `[[npc key=value|...]]` generates an NPC stat block.
- `[[gm_notes Name]]` creates a placeholder/details block for GM note inserts.

Page rendering normally ends in `views/common/page.tpl`, which rebases onto `views/common/base.tpl`. The base template adds the global CSS, banner, top navigation, content shell, footer, table-of-contents behavior, accordions, and glossary initialization.

## Common Routes and Live Tools

`src/common/endpoints.py` owns root-level routes and shared live table tools.

Key routes:

- `/` renders the home page and includes last commit/startup details.
- `/static/<path>` serves static files from `static/`.
- `/media/<path>` serves local media or redirects to a configured Google Cloud Storage bucket.
- `/visual_aid` renders the visual aid display page.
- `/visual_aid_websocket` keeps visual aid clients synchronized.
- `/set_visual_aid` pushes visual aid, iframe, audio, and other display commands to connected clients.
- `/check_visual_aid` and `/upload_visual_aid` support media upload/checking for visual aids.
- `/player soundboard` renders the player soundboard.
- `/player soundboard stats` shows tracked player soundboard use behind GM auth.
- `/get_volume_settings` and `/set_volume` read/update audio volume state.
- `/load_changes` starts a background Git pull; the Bottle reloader restarts if files change.
- `/restart` and `/shutdown` intentionally interrupt the process.
- `/s/<link_type>/<name>` provides shortcut redirects for spells and magic items.
- `/onednd/<url>` redirects to the newer `/dnd/` namespace.

The visual aid system stores current visual state in module globals and broadcasts updates over websockets. Frontend code lives mainly in `static/js/common/visual_aid.js` and `static/js/common/visual_aid_backend.js`.

## D&D Rules Tools

The repo can contain one or more D&D rules namespaces. Existing examples include:

- `dnd`: newer/2024 D&D content.
- `dnd5e`: older 5e content and legacy campaign references.

Both support spell pages, magic item pages, monster pages, search, spell filters, and magic item filters/generators. Much of the structured content is stored as TOML in `data/dnd/` and `data/dnd5e/`.

Important modules:

- `src/dnd/endpoints.py` and `src/dnd5e/endpoints.py`: page/tool routes.
- `src/dnd/utils.py` and `src/dnd5e/utils.py`: spell, magic item, monster loading and filtering.
- `src/dnd/search.py`: namespace search and page-search behavior.
- `src/dnd/api.py`: JSON-ish API routes mounted under `/api/dnd/`.
- `src/dnd5e/magic_item_tracker.py`: magic item tracker expansion used by Markdown pages.
- `src/dnd5e/npc_generator.py`: generated NPC stat blocks.

Templates under `views/dnd/` and `views/dnd5e/` render spell pages, magic item pages, monster sheets, NPC sheets, filter pages, and search pages.

## Campaign Namespaces

Campaign namespaces are usually lighter apps that mostly render Markdown and protect GM notes. The exact set changes over time; check `MODULE_NAMES` and the folders under `data/` for the current list.

Examples of campaign namespace behavior:

- Public pages render from `data/<namespace>/`.
- GM-only pages render from `data/<namespace>/gm_notes/`.
- Some namespaces add specialized routes for campaign-specific tools.

Examples of specialized campaign tools that may exist in a namespace:

- A GM soundboard route or GM insert route.
- A campaign calendar route using a namespace-specific calendar module.
- A synchronized display/control tool, such as Tarokka controls.

GM note protection is implemented per namespace with Bottle `auth_basic()` and a bcrypt hash from `config.ini`.

## Templates and Frontend Assets

The project uses Bottle templates rather than a frontend framework.

Shared templates:

- `views/common/base.tpl`: outer HTML shell.
- `views/common/page.tpl`: Markdown-rendered page wrapper.
- `views/common/top_bar.tpl`: global top navigation.
- `views/common/visual_aid.tpl`: live visual aid display.
- `views/common/player-soundboard.tpl` and `player_soundboard_stats.tpl`: soundboard pages.
- `views/common/light_gallery.tpl`: gallery support.

Namespace templates live under matching folders, such as `views/<namespace>/`, when a namespace needs custom templates.

Frontend code is plain CSS and JavaScript under `static/`. Common JS owns visual aid links, websocket handling, YouTube/audio controls, accordions, table-of-contents toggling, and glossary behavior. Namespace JS handles specialized tools such as spell filters, magic item filters, character sheets, Tarokka cards, and calendars.

## Media Storage

Media is requested through `/media/<path>`.

If the requested file exists locally under `media/`, Bottle serves it directly. If the file does not exist locally and `media bucket` is configured in `config.ini`, the server redirects to:

```text
https://storage.googleapis.com/<bucket>/media/<path>
```

This supports sparse deployments where large media files are not checked out locally on the live server. Media organization currently includes:

- `media/audio/<namespace>/`
- `media/audio/requests/`
- `media/img/visual_aids/<namespace>/`
- `media/img/handouts/<namespace>/`
- `media/img/fanart/<namespace>/`
- `media/img/tarokka/`

## Configuration and Secrets

`config.ini.dist` defines the expected configuration shape. `src.common.utils.load_config()` creates `config.ini` from that file if needed.

Important settings:

- `host`
- `port`
- `run as thread`
- `media bucket`
- `allow http api`
- `GM notes` bcrypt password hash
- `Player soundboard` bcrypt password hash

The source contains default password hashes for local/default use, but runtime values are loaded from `config.ini`.

## Deployment and Operations

Supported operational paths:

- Local or VM Python process: `python main.py`.
- tmux helpers in `makefile`: `start`, `view`, `stop`, and `restart`.
- Docker image based on `python:3.10-slim`.
- Nginx reverse proxy and Certbot HTTPS, documented in `README.md`.
- Google Cloud VM and bucket resources under `terraform/`.
- GitHub Actions workflow that calls `/load_changes` on push.

`/load_changes` uses GitPython to stash local changes, pull from the remote, and rely on Bottle's reloader to restart after code/content changes. Because it mutates the live checkout, it should be treated as an operational endpoint rather than a general API.

## Tests

Tests are under `tests/` and use `unittest`.

Main coverage areas:

- Markdown parser custom syntax and transforms.
- Utility functions.
- Magic item tracker expansion.
- Functional rendering of all Markdown pages under `data/`.

The functional Markdown rendering test is valuable because many site features are content-driven; malformed custom Markdown or broken includes often surface only during page conversion.

## Adding New Content

For ordinary wiki pages:

1. Put public/player-facing Markdown under `data/<namespace>/`.
2. Put GM-only notes under `data/<namespace>/gm_notes/`.
3. Use filenames that match `title_to_page_name()` output: lowercase words separated by hyphens.
4. Link to same-folder pages with `[Page Name]()` when useful.
5. Use `toc: false` front matter when a page should suppress the generated table of contents.

For new namespaces:

1. Create `data/<namespace>/`.
2. Create `src/<namespace>/endpoints.py` with `init(cfg)` and `load_wsgi_endpoints(app)`.
3. Add the namespace to `MODULE_NAMES` in `src/__init__.py`.
4. Add templates or static assets only if the namespace needs custom behavior.
5. Add GM auth routes if the namespace has `gm_notes`.

For new tools:

1. Add server routes in the relevant namespace module or `common` if globally shared.
2. Add Bottle templates under `views/`.
3. Add JavaScript/CSS under `static/`.
4. Keep persistent or generated data under `data/` only if it is content; runtime state files should stay at the root or a dedicated state path.
5. Add or update tests when changing parser behavior, data loading, or reusable utilities.

## Boundaries to Preserve

- `data/<namespace>/gm_notes/` is GM-facing and generally password-protected.
- Adjacent files under `data/<namespace>/` are public/player-facing by default.
- Do not move spoilers, hidden mechanics, private prep, or GM-only notes into public pages.
- Do not copy long source adventure text into notes when a source link and concise table-running summary will do.
- Do not treat `media/` as always locally complete; production may rely on `media bucket` redirects.
