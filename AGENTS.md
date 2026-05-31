# Repository Guidance

This repo is a campaign/wiki site with multiple namespaces under `data`.

## Start Here

- Project architecture: `docs/architecture.md`
- Content authoring and custom Markdown syntax: `docs/content-authoring.md`
- Routing and namespace conventions: `docs/routing-and-namespaces.md`
- Adventure note writing guidance: `docs/adventure-notes.md`
- Reusable GM adventure note template: `docs/adventure-note-template.md`

## Critical Content Boundary

- Each namespace under `data` can contain public player-facing pages and a `gm_notes` folder.
- Pages inside a `gm_notes` folder are GM-facing and generally password-protected.
- Pages adjacent to `gm_notes` are public/player-facing unless the user says otherwise.
- Do not copy spoilers, GM-only details, monster mechanics, hidden plot information, or private prep notes from `gm_notes` into adjacent public pages.

## Common Tasks

- For public/player-facing content, edit files outside `gm_notes`.
- For GM notes, private prep, mechanics, spoilers, or encounter details, edit files inside the relevant `gm_notes` folder.
- For Markdown links, visual aids, sound links, includes, breadcrumbs, tooltips, and front matter, consult `docs/content-authoring.md`.
- For app structure, deployment, and test layout, consult `docs/architecture.md`.
- For routing, namespace setup, GM insert routes, and missing-page debugging, consult `docs/routing-and-namespaces.md`.
- For new GM-facing adventure notes, consult `docs/adventure-notes.md` and use the adventure note template unless the user asks for a different format.

## AI Guardrails

- Do not run mutating git commands unless the user explicitly asks for them or confirms first.
- Read-only git commands are allowed without prompting, such as `git status`, `git diff`, `git log`, `git show`, and `git branch`.
- Mutating git commands include `git add`, `git commit`, `git push`, `git pull`, `git merge`, `git rebase`, `git checkout`, `git switch`, `git reset`, `git restore`, `git stash`, and tag/branch creation or deletion.
- Never revert, discard, or overwrite user changes unless the user explicitly asks for that exact action.
- When the worktree has unrelated modifications, leave them alone and mention them only if they affect the task.
- Prefer documenting assumptions and making narrow edits over broad cleanup or opportunistic refactors.
- Do not make broad formatting-only changes unless the user asks for them.
- Do not delete, rename, or reorganize files/directories unless the user explicitly asks or confirms.
- Do not clean generated files, caches, media, backups, or dependency folders unless asked.
- Do not move GM-only spoilers or mechanics into public/player-facing pages.
- Do not normalize ad hoc route/content patterns just because they are inconsistent; document or ask first.
- Do not start long-running servers or watchers unless needed for the task. If one is started, report it clearly.
- When summarizing external adventure/source material, prefer concise summaries and links over copying source text.

## External Adventure Sources

- D&D adventure source JSON may live outside this repo at `..\5etools-src\data\adventure`.
- The wiki repo can link to rendered 5e.tools adventure pages, such as `https://5e.tools/adventure.html#...`, for full room descriptions and source text.
- Prefer concise summaries and table-running notes over copying large sections of adventure text.
