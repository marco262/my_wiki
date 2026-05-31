# Routing and Namespaces

This document describes the current routing and namespace patterns in the repo. These are conventions, not hard rules. The project has grown as a sandbox/learning project, so many endpoints were added ad hoc. Future namespaces can break existing patterns when a clearer design is useful.

Use this as a map of how the current app is wired and a checklist for common namespace changes.

## Source of Truth

The active namespace list lives in `src/__init__.py`:

```python
MODULE_NAMES = [...]
```

`src.__init__.load_wsgi_endpoints()` loops over that list.

For each name:

1. It imports `src.<name>.endpoints`.
2. It calls `module.init(cfg)`.
3. If the name is `common`, routes are loaded directly onto the root Bottle app.
4. Otherwise, a child `Bottle()` app is created and mounted at `/<name>/`.
5. If `src.<name>.api` exists, it is mounted at `/api/<name>/`.

The enabled namespace list can change over time. Check `MODULE_NAMES` rather than relying on documentation examples.

## Namespace Shape

A namespace often has some or all of these:

```text
src/<namespace>/endpoints.py
src/<namespace>/api.py
data/<namespace>/
data/<namespace>/gm_notes/
views/<namespace>/
static/js/<namespace>/
static/css/<namespace>.css
media/img/visual_aids/<namespace>/
media/audio/<namespace>/
```

Only `src/<namespace>/endpoints.py` is required for an enabled namespace. Everything else is optional and should exist only when the namespace needs it.

## Common Campaign Pattern

Many campaign namespaces follow this pattern:

```python
def init(cfg):
    ...

def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @app.get("/home")
    def home():
        return md_page("Home Page Title", "<namespace>")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "<namespace>")

    @app.get("gm_notes/<name>")
    @view("common/page.tpl")
    @auth_basic(gm_notes_auth_check)
    def gm_notes(name):
        return md_page(name, "<namespace>", directory="gm_notes")
```

This gives:

```text
/<namespace>/                namespace home page
/<namespace>/home            same or similar home page
/<namespace>/<name>          public page from data/<namespace>/<name>.md
/<namespace>/gm_notes/<name> GM page from data/<namespace>/gm_notes/<name>.md
```

Several namespaces also support categorized public pages:

```python
@app.get("<category:path>/<name>")
def category_page(category, name):
    return md_page(name, "<namespace>", directory=category)
```

That enables:

```text
/<namespace>/<category>/<name>
```

to resolve to:

```text
data/<namespace>/<category>/<name>.md
```

## GM Notes

GM notes are protected per namespace with Bottle `auth_basic()`.

The common pattern:

```python
GM_NOTES_PW_HASH = ...

def init(cfg):
    global GM_NOTES_PW_HASH
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")

def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
```

Routes inside `gm_notes` should use `@auth_basic(gm_notes_auth_check)` unless they are intentionally public.

The important content boundary:

- `data/<namespace>/gm_notes/` is GM-facing and generally private.
- Files adjacent to `gm_notes` are public/player-facing by default.

## GM Note Inserts

Some namespaces support inline GM-only inserts inside public pages using `[[gm_notes Name]]`.

For this to work, the namespace needs:

1. A route:

   ```python
   @app.get("gm_notes/insert/<name>")
   @auth_basic(gm_notes_auth_check)
   def gm_notes_insert(name):
       return md_page(name, "<namespace>", directory="gm_notes/inserts", load_template=False)
   ```

2. Insert files:

   ```text
   data/<namespace>/gm_notes/inserts/<generated-id>.md
   ```

3. Page JavaScript:

   ```html
   <script type="module">
       import {init_gm_notes_inserts} from "/static/js/common/gm_notes.js";
       init_gm_notes_inserts("<namespace>");
   </script>
   ```

The generated ID is based on the insert title. For `[[gm_notes Secret Door]]`, the fetch target is:

```text
/<namespace>/gm_notes/insert/secret-door
```

and the expected file is:

```text
data/<namespace>/gm_notes/inserts/secret-door.md
```

## Root Common Routes

`common` is special. It is not mounted under `/common/`; it installs routes directly on the root app.

Important common routes include:

```text
/                         home page
/static/<path>            static files
/media/<path>             local media or bucket redirect
/visual_aid               visual aid display
/visual_aid_websocket     visual aid websocket
/set_visual_aid           visual aid/audio command endpoint
/player soundboard        player soundboard page
/player soundboard stats  GM-only soundboard stats
/load_changes             git pull/reload operational endpoint
/s/<link_type>/<name>     shortcut redirects
/onednd/<url>             redirect to /dnd/<url>
```

Because these are root routes, be careful when adding new common routes. They can collide with mounted namespace paths or future root pages.

## Rules and Tool Namespaces

Rules/tool namespaces often use explicit routes instead of the general campaign-page pattern.

Examples of explicit route categories:

```text
/<namespace>/class/<name>
/<namespace>/race/<name>
/<namespace>/spell/<name>
/<namespace>/monster/<name>
/<namespace>/equipment/magic-item/<name>
/<namespace>/spell_filter
/<namespace>/site_search
```

These routes often load structured data from TOML or JSON and render specialized templates rather than simple Markdown pages.

API routes are optional. If a namespace has `src/<namespace>/api.py`, it should expose:

```python
def load_api_endpoints(app: Bottle):
    ...
```

and the loader mounts it under:

```text
/api/<namespace>/
```

## Specialized Namespace Tools

Some namespaces add special routes for campaign tools. Existing patterns include:

- calendar routes backed by namespace-specific calendar modules
- soundboard routes
- websocket-backed display/control tools
- custom generator routes
- private insert routes

These are intentionally flexible. Prefer a clear route that matches the tool over forcing every namespace into the same shape.

## Route Matching Notes

Bottle route order matters. Broad routes like:

```python
@app.get("<name>")
@app.get("<category:path>/<name>")
```

can catch paths that might otherwise be intended for more specific routes. In namespace files, define specific tool routes before broad catch-all page routes when there is any chance of conflict.

Also note that some existing routes use leading slashes and some do not:

```python
@app.get("/calendar")
@app.get("gm_notes/<name>")
```

Both styles appear in the repo. When editing existing endpoints, match nearby style unless there is a reason to clean it up.

## Adding a Namespace

Recommended minimal steps:

1. Create `src/<namespace>/endpoints.py`.
2. Define `init(cfg)` even if it only does `pass`.
3. Define `load_wsgi_endpoints(app: Bottle)`.
4. Add the namespace name to `MODULE_NAMES` in `src/__init__.py`.
5. Create `data/<namespace>/` and at least one home page if the namespace renders Markdown.
6. Add `data/<namespace>/gm_notes/` only if the namespace needs private GM pages.
7. Add templates, static assets, media folders, or an API module only if needed.

A simple public-only namespace can be very small:

```python
from bottle import Bottle
from src.common.utils import md_page

def init(cfg):
    pass

def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        return md_page("Home", "<namespace>", build_toc=False)

    @app.get("<name>")
    def page(name):
        return md_page(name, "<namespace>")
```

## Removing a Namespace

Recommended checks:

1. Remove the name from `MODULE_NAMES`.
2. Decide whether to delete or archive `src/<namespace>/`.
3. Decide whether to delete or archive `data/<namespace>/`.
4. Check `views/<namespace>/`, `static/js/<namespace>/`, `static/css/`, and `media/.../<namespace>/` for namespace-specific assets.
5. Search for links to `/<namespace>/` in `data/`, `views/`, and `static/`.
6. Update navigation, especially `views/common/top_bar.tpl`, if it links to the namespace.

## Debugging a Missing Page

If a URL does not resolve:

1. Confirm the namespace is listed in `MODULE_NAMES`.
2. Confirm `src/<namespace>/endpoints.py` has a matching route.
3. Confirm the content file exists under the expected `data/<namespace>/...` path.
4. Confirm the filename matches `title_to_page_name()`.
5. For categorized pages, confirm the namespace has a `<category:path>/<name>` route.
6. For GM pages, confirm you are authenticated and the route uses `directory="gm_notes"`.
7. For GM inserts, confirm the route, JS initializer, generated ID, and insert file all exist.
8. For template-rendered pages, confirm the relevant file exists under `views/`.

## Design Guidance for Future Routes

Existing patterns are useful but not sacred.

When adding a future namespace or tool:

- Prefer clarity over matching an old ad hoc route.
- Keep public and private content boundaries obvious.
- Put shared behavior in `common` only when it really applies globally.
- Use explicit routes for tools and structured data.
- Use broad Markdown page routes for simple content namespaces.
- Avoid catch-all routes before specific tool routes.
- Document intentional deviations in this file or near the endpoint code.
