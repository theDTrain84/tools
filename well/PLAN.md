# The Well · plan v1 (October 2, 2026)

*Written by Mise from Dustin's ask (Telegram, 5:11 PM): a game and reflection space in the DNSC style, elevated, paper, the same tones, grown from what we already built. Working name from his own line: "the well is deep."*

## What it is
A room under Teaching & tools at tools.dnsc.ai/well/. Two kinds of things live there:

1. **Small daily games that teach the vocabulary of working with AI.** Five minutes, paper, no account. New things require new vocabulary (his line, 9/21); the games are how people learn it without a lecture.
2. **Quiet rooms for the people in your day.** The descent from Gumbo City, brought up into paper: the rooms with no streaks and no metrics, where you hold people in your thoughts and then leave.

The laws, carried over from the Stillness Sanctuary and the World Tree in Gumbo City: no streaks you have to keep, no metrics, no feeds, no urgency, the room encourages you to leave when complete, nothing is stored or sent. (Source: ~/Claude/MOSGumboCity/js/sanctuary-ui.js, world-tree-ui.js.)

## What we harvested (the well)
| From | What | Where it went |
|---|---|---|
| World Tree, "the Between Space" | people from your day float in orbit; tap one to hold them in your thoughts; no DM, no reply | **The Walk-in**: the ring with one seat per person you name, a breath, one line |
| Stillness Sanctuary | the laws (no streaks, no metrics, leave when complete), "Something here loves me without needing anything from me" | the hub's law line and every room |
| River of Release | write what is heavy onto a leaf, the water carries it, nothing stored | **The River** (next) |
| Forest of Remembrance | a 15-minute walk with at most six soft prompts | **The Walk** (later): a paced reading of six questions |
| Observatory of Awe | real moon phase, sunrise, sunset | folds into Lunar rhythms (later) |
| Elemental branding | light, salt, love, fire, water, earth; ElementField motes and grain | the Walk-in's element picker and canvas field; each game gets an element |
| ol' Dusty's Arcade | one row in a manifest adds a game; local iframes; "PRESS START" | the hub's card grid is the manifest; each game is its own folder |
| The Pass / Give It a Soul | the human gate, the four soul things (context, personality, responsibility, purpose) | future games: The Gate (approve or deny the agent's request), Four Things |
| Recipe cards | the prompt, the rules, the rhythm | every game ends with a two-sentence teaching, the same register |

## The prototypes (built tonight)
- `/well/` · the hub. Paper, two grids: today's games, the quiet room. Law line. Lineage paragraph.
- `/well/daily-line/` · **The Daily Line**: 5×5 crossword on AI vocabulary, one a day, with a teaching note on finish, keyboard and touch, bank of 14 grids, streak kept quietly in the browser only.
- `/well/five-moves/` · **Five Moves**: twenty cards, sort to Listen, Map, Build, Trust, Teach; a solved move opens its one line; four mistakes; bank of 10 sets.
- `/well/walk-in/` · **The Walk-in**: dusk room, element field, the ring; name people, each takes a seat; a 4-2-4 breath cue in step with the ring; one line for all of them; close the room. Local only, empties tomorrow.

## Next, in order (each a day or less)
1. His review of the three, then publish to the tools repo (`git push` deploys in about a minute) and a card on the Framer /tools page.
2. **The River** (letting go) and **The Glossary** (flip cards: the term, the plain sentence, the one line from the site).
3. **The Gate**: a one-minute daily game, approve or deny an agent's request, spot the one that should not pass; teaches the human gate.
4. Elemental styling per game (light for the Line, fire for Five Moves, water for the River).
5. Later, if he wants it: a Framer-embedded strip on Home ("Today in the Well"), and the lunar layer.

## How to add a thing
One folder under `well/` with an `index.html`, the shared shell (`../../assets/site.css`, nav, footer, crumb), fonts via Google Fonts, no external JS, everything in one file, a card on `well/index.html`. Daily content is a bank in the file, picked by day number from 2026-10-02. Keep each under 70 KB. Phone first. No em dashes in copy. The site says "we."
