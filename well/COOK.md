# The daily cook · crossword recipe (v0, 10/2/26, b3)

*How Mise cooks two fresh crosswords each morning for The Well, starting Monday, October 5. Write-up only: the builder isn't built yet. Pairs with PLAN.md.*

## The two tracks
| Track | Page | What it teaches | Grid |
|---|---|---|---|
| **learning** | `/well/daily-line/` (The Daily Line) | the vocabulary and practice of working with AI | 5×5 today, 7×7 when the builder lands |
| **news** | `/well/morning-edition/` (The Morning Edition) | what actually happened in AI yesterday | 7×7 |

Both tracks share one engine, one JSON format and one cook. Only the inputs and the voice of the clues differ.

## Inputs (gathered fresh each morning)
1. **Yesterday's AI news, from primary sources only.** Company and lab announcements, official docs and changelogs, government filings and press releases, the paper itself (arXiv), and named reporting from outlets that link their sources. Aggregators and summary posts are fine for finding stories, but the facts in a clue come from the primary page. Keep 5 to 8 stories, each with: headline, one-line fact, the primary URL, and 1 to 3 candidate answer words (a company, a product, a concept, a number spelled out).
2. **The practice lexicon** (learning track): the house words with their one-line meanings. Seed it from the Daily Line bank, the One Word bank (`/well/one-word/`) and the /teaching page (agent, token, close, ledger, wake, loop, lines, table, human in the loop, LEAD, Listen/Map/Build/Trust/Teach, the three rings…). Store it as `well/cook/lexicon.json` so it grows over time.
3. **A curated fill list.** Common English words, 3 to 7 letters, family-safe, with no obscure crosswordese (no ESNE, ETUI, ALAI). Start from a public-domain frequency list cut to the top ~20k, then strip anything awkward by hand once. Store it as `well/cook/fill.txt`, one word per line, uppercase.
4. **Yesterday's two puzzles,** so no answer repeats within 14 days.

## The builder (plain Python, no dependencies)
`well/cook/build.py --track news --date 2026-10-05`

1. **Pick the theme words.** News track: 2 to 4 words from the day's stories (answer words, 3 to 7 letters). Learning track: 2 to 3 lexicon words, rotated so each comes back about once a month. The longest theme word becomes the **teaching word** (`w`).
2. **Choose a template.** Keep a small library of 7×7 black-square patterns (about 12): rotationally symmetric, 6 to 12 black squares, no entry shorter than 3, every white square checked both ways (in an across and a down entry). Patterns live in `well/cook/templates.json`.
3. **Seed the theme.** Try placing each theme word into a slot of matching length, longest first, across and down.
4. **Fill by backtracking.** Repeat until full:
   - Pick the open slot with the fewest candidates (most-constrained first).
   - Candidates come from theme words, then the lexicon, then the fill list, matched by pattern (for example `T?K?N`).
   - Order them by a score: theme > lexicon > common fill. Never reuse a word inside one grid, and skip anything used in the last 14 days.
   - Place a word, then forward-check every crossing slot: each must still have at least one candidate. If not, undo and try the next word.
   - Cap the search at about 200k steps per template, then move to the next template. If every template fails, drop the shortest theme word and try again.
5. **Verify.** Re-derive every across and down entry from the finished grid and confirm each is a real word from the lists. Confirm every white square is checked both ways, no word repeats, and the teaching word is in the grid. It's the same check the page's self-test runs.
6. **Write clues.** Mise writes them, never the script:
   - News track: every theme clue states one checked fact from the primary source, with the URL stored next to it.
   - Learning track: clues teach, in the register of the Daily Line bank.
   - Fill clues stay plain, short and warm.
   - No em dashes, no "not X but Y" constructions, and the site says "we."
7. **Write the teaching note** (`n`): two or three sentences on the teaching word, in the Recipe Book voice.
8. **Emit the JSON** (schema below), then commit `well/daily-line/puzzles/YYYY-MM-DD.json` and `well/morning-edition/puzzles/YYYY-MM-DD.json`. A push goes live in about a minute.

**Rhythm.** A session cron at about 5:30 AM ET on weekdays (rebuilt on wake like the others) cooks both puzzles. If the cook fails, the pages quietly fall back to the bank. Mise posts one line to Telegram only if something failed.

## Puzzle JSON schema
One file per track per day, at `<track page>/puzzles/YYYY-MM-DD.json`:

```json
{
  "v": 1,
  "track": "news",                       // "learning" | "news"
  "date": "2026-10-05",                  // the day it's for, local ET
  "no": 4,                               // display number (days since 2026-10-02, plus 1)
  "size": 7,                             // grid is size × size
  "g": ["###SCAN", "#....."],            // rows: letters A–Z, "#" for black. Same as the bank's g, any size
  "a": [["SCAN", "Clue text", {"src": "https://…"}]],   // across, reading order; third item optional
  "d": [["SEAT", "Clue text"]],          // down, reading order
  "w": "AGENT",                          // teaching word, must appear in g
  "n": "Two or three sentences that teach the word.",
  "sources": [                           // news track: required; learning track: optional
    {"title": "What happened, in our words", "url": "https://primary.source/…", "date": "2026-10-04"}
  ],
  "cooked": "2026-10-05T09:31:00Z",      // when Mise built it
  "checked": true                        // the builder's verify step passed
}
```

**Rules the page enforces on load:**
- The page re-runs the self-test on the loaded file: the answers derived from `g` must match `a` and `d`, every white square must be checked both ways, there are no dashes, and `w` must be in the grid.
- If the file fails, or doesn't exist (404, offline), the page uses the bank exactly as today and logs one console warning.

## The small change the page needs
Today `daily-line/index.html` has `5` hard-coded throughout, and builds the puzzle synchronously from `BANK`. The change:

1. **Make size come from the grid.** Set `N = P.g.length`, then replace every literal `5` and `4` in the engine with `N` and `N-1`:
   - `slotsOf`, `selfTest`, the numbering loop and the DOM build
   - `move()`, where `r>4`/`c>4` become `r>N-1`
   - the CSS `grid-template-columns: repeat(5, var(--cell))`, set from JS via `gridEl.style.gridTemplateColumns`
   - a smaller `--cell` when N is 7, so a 7×7 grid still fits a 360px phone (about 44px cells)
2. **Load today's file first.** Wrap the setup (from `/* ---------- model ---------- */` down to the end) in `start(P)`. Then:
   ```js
   fetch("puzzles/" + isoToday + ".json", {cache: "no-store"})
     .then(r => r.ok ? r.json() : Promise.reject())
     .then(p => selfTestOne(p) ? start(p) : start(bankPick()))
     .catch(() => start(bankPick()));
   ```
   `selfTestOne` is today's `selfTest` loop body pulled out to check a single puzzle.
3. **Key storage by date as well as day index:** `dnsc-daily-line-state` should hold `{date, …}`, so a cooked puzzle and the bank puzzle for the same day never mix answers.
4. **Show the sources on finish.** If `P.sources` exists, render it under the teaching note as a short list of links ("Where this came from").

## Morning Edition as a second page: what to factor out
Recommendation: one shared engine file, with two thin pages on top of it.

**Move into `well/assets/crossword.js`:**
- **The engine:** everything inside the current IIFE except the `BANK`, the copy and the element ids it writes text into.
- **Its public surface:** `Crossword.mount({ root, track, bank, startDate, storagePrefix, puzzlePath, labels })`, which handles the fetch-or-bank load, the self-test, the grid, the clue lists, the on-screen keyboard, check/reveal, the clock, the done card and the aria-live region.
- **Size-agnostic code throughout** (the N change above).
- **Storage keys from `storagePrefix`**, so `dnsc-daily-line-*` and `dnsc-morning-edition-*` never collide.
- **The streak and best stats in the done card become optional** (`labels.stats: false`). The Well's law is "no streaks you have to keep", and the Daily Line currently shows "Streak / Best". Turn stats off on both pages and keep only the quiet solve time.

**Move into `well/assets/crossword.css`:** the grid, cell, clue, keyboard, done-card and toolbar styles from the Daily Line `<style>` block, with `--cell` set per size. The page keeps only its own tokens and accents. Morning Edition gets sky as its accent (`--accent: var(--sky)`), and Daily Line keeps gold.

**Each page keeps:**
- the shell (nav, crumb, footer, motes)
- its header copy
- its own fallback `BANK`: Morning Edition's bank can be a handful of evergreen "how to read AI news" grids for days the cook doesn't run, such as weekends
- a single `Crossword.mount(...)` call

**Morning Edition specifics:**
- Eyebrow "The Well · AI in the news".
- The date line reads "News from <yesterday's date>".
- Each theme clue gets a small "source" link after you solve, never before, so the links don't give answers away.
- The teaching note becomes "What it means for your work": one plain sentence per story.

**Order of work:**
1. Factor the engine out with the Daily Line still working exactly as today. A visual check plus its self-test passing is the gate.
2. Add the size change and the fetch-with-fallback.
3. Build `/well/morning-edition/` on the shared engine with its fallback bank.
4. Build `well/cook/` (lexicon, fill list, templates, `build.py`) and cook the first two puzzles by hand on Monday, checking every crossing.
5. Only then wire the 5:30 AM cron.
