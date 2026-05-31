# Adventure Notes

This guide explains how to turn a published adventure, outline, or homebrew scenario into GM-facing table notes.

The reusable template lives at:

```text
docs/adventure-note-template.md
```

Use that template for new GM adventure pages unless the user asks for a different shape. This document explains the working style behind the template.

## Goal

Adventure notes should help the GM run the session at the table. They should not be a rewritten copy of the module.

Good adventure notes answer:

- What is happening?
- What should happen next?
- Who is present?
- What do the players need to learn or decide?
- What mechanics matter right now?
- Where is the full source if I need details?
- What has been changed for this campaign?

They should avoid:

- copying long source text
- scattering the same NPC or monster details across multiple scenes
- hiding critical plot flow in paragraphs
- turning every room into a full rewrite
- mixing public/player-facing hooks with GM spoilers

## Start With Source Understanding

Before writing notes, inspect the source adventure enough to understand:

- the premise
- the intended level range
- the expected sequence of events
- key NPCs and factions
- key locations
- monsters, hazards, and encounter mechanics
- clues and required information
- failure states and consequences
- rewards and aftermath

If the adventure is from 5e.tools or another external source, prefer linking to the rendered source page or specific section instead of copying the text.

Example source links:

```text
https://5e.tools/adventure.html#kftgv,1
https://5e.tools/adventure.html#kftgv,1,varkenbluff%20museum%20of%20natural%20history
```

## Keep the Top Useful

The top of the page should be the GM's quick reorientation point.

Use **Quick Reference** for:

- source link
- intended level range
- actual party level
- expected length
- adventure type
- tone
- premise
- main stakes
- failure consequence
- campaign hook

Use **Global Assets and Source Links** for links that are useful across the whole adventure:

- recurring visual aids
- general ambience playlists
- overview maps
- source links
- rules references

Put visual aid and sound links where the GM is most likely to click them during play. For example, an NPC portrait belongs in that NPC's entry and in any scene where the NPC is introduced; a room image or ambience track belongs in that room or scene. Use the global section for assets that are reused often, for prep inventory, or for links that do not belong to one specific scene.

## Adventure Flow

The Adventure Flow section is the expected plot outline. It should be short and readable during play.

Write it as beats, not prose:

1. Opening hook
2. Inciting problem
3. Investigation or approach
4. Complication
5. Main challenge, dungeon, or heist
6. Finale
7. Aftermath

Each beat should say:

- what changes
- what the players are likely trying to do
- what information or decision moves the story forward
- what scene or location likely comes next

This is the section to check when the table goes off-script and the GM needs to recover the adventure's direction.

## Scene Notes

Scene notes are the main running surface.

Each scene should have a clear purpose. If a scene does not change the situation, reveal information, create a decision, or create pressure, it probably does not need a full scene entry.

Use scene notes for:

- setup
- source link
- visual aid or music
- NPCs present
- player goals
- clues and information
- mechanics
- combat or hazard references
- exit paths
- ways to unstick the scene

Scene notes should link to reusable sections:

```md
**NPCs Present:**

- [Cassee Dannell](#cassee-dannell)

**Combat / Hazard Notes:**

- [Aberrant Egg](#aberrant-egg)
```

Do not repeat full NPC motives, stat block details, or monster tactics in every scene where they appear. Put those in the NPC or Monsters and Hazards section.

## Clues and Mysteries

For mysteries, investigations, heists, and social adventures, add a Clue Tracker.

Use it to prevent essential information from being spread only through scene prose.

Track:

- clue
- where it can be found
- what it points to
- whether it is required
- backup delivery method

Required clues should usually have more than one delivery path. If the players miss a required clue, the notes should say how the GM can still move the adventure forward.

Good fail-forward options:

- an NPC volunteers partial information
- a rival makes a move
- time pressure forces the next event
- a failed check reveals the clue but adds a complication
- a different skill or resource can uncover the same lead

## NPCs

Use a separate NPC section for named social characters, suspects, patrons, allies, recurring enemies, and anyone likely to be referenced from more than one scene.

Good NPC entries are short and table-useful:

- role
- appears in
- wants
- knows
- personality
- how they treat the party
- what they reveal if trusted, pressured, or exposed
- source, portrait, or stat block link

For a school campaign, include how the NPC treats student adventurers when that affects the scene.

Avoid biography unless it matters at the table.

## Monsters and Hazards

Use a separate Monsters and Hazards section for combat creatures, traps, curses, environmental effects, and special rules.

Each entry should include:

- where it appears
- stat block or rules link
- role in the adventure
- tactics or behavior
- rules to preload
- party-specific adjustments
- short table description

This section is for running encounters quickly. It does not need to reproduce a full stat block if a reliable source link exists.

When adjusting encounters, document the change and the reason:

```md
**Adjustments for This Party:** Party is level 4 instead of level 1. Increase guard HP, add one extra minion, and keep the monster's damage unchanged to avoid swingy one-shots.
```

## Locations

Use a Locations section when a place matters across multiple scenes or has tactical/social rules.

Include:

- source link
- map or visual aid
- purpose
- public information
- secrets
- security or obstacles
- notable features
- connected scenes

Do not create location entries for every room unless the adventure is a room-by-room dungeon crawl and the locations matter independently.

For dungeon crawls, consider grouping rooms by zone instead of copying every room.

## Rewards and Aftermath

Rewards and aftermath should be easy to find at the end of a session.

Track:

- expected rewards
- optional rewards
- school consequences
- NPC follow-up
- unresolved threats
- future hooks

If the adventure is part of a campaign, use this section to note what might matter later.

## Campaign Adaptation

Use Campaign Adaptation Notes for anything changed from the published adventure.

Common adaptation notes:

- school framing
- why the students are involved
- why adult NPCs do not solve the problem
- tone adjustments
- content adjustments
- level and balance adjustments
- continuity links to past or future sessions

Do not hide important adaptation changes only inside scene text. If the published adventure says one thing and the campaign version says another, document the difference here.

## Public Adventure Options vs GM Notes

Keep player-facing adventure option pages spoiler-light.

Player-facing pages can include:

- premise
- tone
- broad adventure type
- expected length
- intended level range
- player-facing tags

GM notes can include:

- spoilers
- hidden villains
- clue structure
- stat block links
- encounter mechanics
- traps and hazards
- source-section links
- adaptation notes
- balance changes

If the same adventure has both pages, edit the public and GM versions separately and preserve the privacy boundary.

## Visual Aids and Sound

Prefer placing visual aid and sound links at the point of use.

Most of the time, that means:

- scene-specific room art in the scene note
- NPC portraits in the NPC entry and the NPC's introduction scene
- monster art in the monster entry and the encounter scene
- combat music in the combat scene
- location ambience in the location or exploration scene

A top-level asset list is still useful when:

- the same asset is reused across many scenes
- the GM wants a prep checklist of available assets
- a map, playlist, or source link applies to the entire adventure
- the asset does not have one obvious scene home

The tradeoff is navigation. A central list is tidy and helps prep, but it can force the GM to scroll away from the scene during play. Inline links are better for running the table, but they can become noisy if every scene repeats the same links. Prefer inline links for moment-of-use assets and central links for global/reusable assets.

Common visual aid categories:

- location exterior
- tactical map
- key NPC portraits
- important object
- monster or final threat
- handout

Common sound categories:

- arrival / field trip
- investigation
- stealth or heist
- tension
- combat
- aftermath

Use the custom syntax documented in `docs/content-authoring.md`.

## Source Links

Use source links aggressively, but keep them purposeful.

Good places for source links:

- Quick Reference source
- global source links
- scene source link
- location source link
- monster/stat block source link

When linking to 5e.tools, use the most specific useful section if possible. The point is to let the GM jump to the full text only when needed.

## How Much Detail

Use this rough scale:

- **One-shot:** concise flow, compact scene notes, only essential NPCs and monsters.
- **Short adventure:** full quick reference, flow, scene notes, clue tracker if relevant, reusable NPC/monster sections.
- **Medium adventure:** stronger location structure, more explicit aftermath, and more detailed adaptation notes.
- **Dungeon crawl:** zones and room groups may matter more than social scenes.
- **Mystery/heist:** clue tracker and failure handling matter more than room-by-room summaries.

The more nonlinear the adventure, the more useful the Clue Tracker, NPCs, Locations, and fail-forward notes become.

## Workflow for Creating Notes

Recommended process:

1. Read or inspect the source enough to understand the full plot.
2. Write Quick Reference.
3. Add source links and obvious assets.
4. Draft Adventure Flow.
5. Identify key scenes.
6. Extract NPCs into the NPC section.
7. Extract monsters and hazards into their section.
8. Build a Clue Tracker if information flow matters.
9. Add locations only where they help.
10. Add adaptation notes for the campaign.
11. Fill the prep checklist.
12. Remove repeated information.

The last step matters. If the same NPC goal, stat block link, or rule appears in three places, move it to a reusable section and link to it.

## Common Mistakes

- Writing a second version of the module instead of table notes.
- Putting the plot outline only in scene prose.
- Repeating NPC details in every scene.
- Forgetting failure paths for required clues.
- Hiding balance changes in encounter notes only.
- Mixing public player hooks with GM spoilers.
- Adding every source room as its own note even when most rooms are straightforward.
- Leaving source links out, which forces the GM to search mid-session.

## When to Deviate From the Template

The template is a default, not a constraint.

Deviate when the adventure format calls for it:

- A pure dungeon crawl may need a zone/room index.
- A social intrigue adventure may need a relationship map.
- A sandbox may need fronts, factions, clocks, and location tables.
- A heist may need security layers and route options.
- A mystery may need clue redundancy and suspect summaries.
- A large campaign arc may need session-by-session notes.

When deviating, keep the same principle: put reusable facts in one place and make the active table-running surface easy to scan.
