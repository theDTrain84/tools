# Monday morning, the news step (10/5/26 and every weekday after)

The learning track for Monday is already cooked: `daily-line/puzzles/2026-10-05.json` (7×7, teaching word MISTAKE). Only the news track remains.

1. **Gather (15 min).** Pick 5 to 8 AI stories from the last news day. On a Monday that means Friday through Sunday. Primary sources only: the lab or company announcement, the docs or changelog, the government filing or press release, the paper itself. For each story, note: what happened in one line (documents and dates, **never people's names**), the primary URL, and 2 or 3 candidate answer words of 3 to 7 letters.
2. **Build (1 min).** From `well/cook/`:
   `python3 build.py --track news --date 2026-10-05 --theme WORD1,WORD2,WORD3 --seed 1 > /tmp/news.json`
   It places a 5-letter theme word most of the time and prefers the others. If none land, try `--seed 2`, `3`, `4`, or change the theme words. Pick the grid whose fill is cleanest and that holds at least one news word.
3. **Hand-check (5 min).** Read every across and down answer aloud. Swap out anything obscure, any proper noun and any abbreviation by re-running with a new seed. Mise is the gate here, never the script.
4. **Clue (15 min).** News answers get one checked fact from the primary source, with `{"src": URL}` as the clue's third item. Fill clues stay plain. No em dashes, no "not X but Y", no people's names. Write `n`, the teaching note: what it means for your work, two or three sentences. Fill `sources` with a title in our words, the URL and the date for each story used. Set `w` to the strongest news word that landed.
5. **Verify.** `node -e 'global.window={};global.document={};require("../assets/crossword.js");console.log(window.Crossword.check(require("/tmp/news.json")))'` must print `[]`.
6. **Ship.** Save to `morning-edition/puzzles/2026-10-05.json`, commit, push (it's live in about a minute), then open the page once to confirm it says "News from …" and not "How to read the news".

If anything fails, do nothing: the page falls back to the evergreen bank on its own.
