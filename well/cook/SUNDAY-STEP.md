# Sunday afternoon, the weekly step (every Sunday from 10/11/26)

The Sunday Edition goes live at 6 PM ET: one 11×11 crossword on the week's AI news (Sunday to Saturday, plus today), with a short list of what's coming in the next seven days. Start at 4:30 PM. The page lives at `well/sunday-edition/`, and edition No. 1 (`puzzles/2026-10-04.json`) is the worked example to copy.

1. **Research (4:30 to 5:05).** Two lists, primary sources only, written into `well/sunday-edition/research/YYYY-MM-DD.md` (the Sunday's date) with URLs:
   - **The week:** 8 to 12 AI stories from the last seven days. Company and lab announcements, model cards and changelogs, government press releases and filings, committee pages and testimony, the paper itself. Aggregators help you find a story; the fact comes from the primary page. For each: the date, one plain line (documents and dates; never characterize a person), the URL, whether you opened it yourself, and 2 to 4 candidate answer words (5 to 8 letters lands best; common words beat names).
   - **Coming this week:** 3 to 5 dated items for Monday to Saturday ahead: hearings, launches, earnings, conferences, deadlines. Only items with a dated source page.
   - Press-only stories can sit in the research file, marked as press only. They never become clues.

2. **Build (5:05 to 5:15).** From `well/cook/`:
   ```
   python3 build.py --track weekly --size 11 --date YYYY-MM-DD \
     --must WORD1 --theme WORD2,WORD3,...(20 to 30 candidates) \
     --recent JUNK1,JUNK2 --seed 1 --budget 420 --want 9 > /tmp/sun.json
   ```
   - `--must` holds the one or two words the week can't go without; every kept grid has them.
   - Give `--theme` every candidate word from the research, 20 to 30 of them. The builder keeps the grid that holds the most theme words with the least last-resort fill, and lists `_theme_placed` and `_theme_missed`.
   - Run four to eight seeds in parallel (`--seed 1` to `8`, each to its own file) and keep the cleanest. Six or more theme words is a good week.
   - `--recent` bans words: anything obscure, any proper noun you don't want, anything that came up in the last month.
   - `--size 13` works too, but it fills far less often. Use it only on a big week with time to spare.

3. **Hand-check (5:15 to 5:20).** Read every across and down answer aloud. If something is obscure, awkward or a name, add it to `--recent` and run again. Words from `fill-extra.txt` (the last-resort list) get the hardest look. Mise is the gate here, never the script.

4. **Clue (5:20 to 5:40).**
   - **Theme clues** state one checked fact from the primary page, with `{"src": URL}` as the third item.
   - **Fill clues** stay plain, short and warm.
   - No em dashes and no "not X but Y". The site says "we". No person is characterized, and no Collective research numbers appear.
   - Set `no` to the edition number (1 on 2026-10-04, then plus one each week).
   - Set `w` to the strongest theme word.
   - Write `n`, the teaching note: two or three sentences in the Recipe Book voice.
   - Fill `sources` with a title in our words, the URL and the date for each story you used.
   - Fill `coming` with 3 to 5 items, each as `{"date": "YYYY-MM-DD", "end": "YYYY-MM-DD"?, "text": "…", "url": "…"}`. Keep answer words out of the coming text, because that list shows before the solve.
   - Delete the `_theme_*` keys and set `"checked": true` and `"cooked"`.

5. **Verify (5:40 to 5:45).**
   ```
   node -e 'global.window={};global.document={};require("../assets/crossword.js");console.log(window.Crossword.check(require("/tmp/sun.json")))'
   ```
   This must print `[]`. Then search the file for em and en dash characters; there should be none.

6. **Ship (by 5:55).**
   - Save the file as `sunday-edition/puzzles/YYYY-MM-DD.json` and add `{"date": "YYYY-MM-DD", "no": N}` to `sunday-edition/puzzles/index.json`.
   - Copy the research file into place, then commit and push. It goes live in about a minute.
   - At 6 PM, open `https://tools.dnsc.ai/well/sunday-edition/` once and confirm the date line reads "The week of …" with the right No.

**If anything fails, do nothing.** The page shows the newest edition listed in `puzzles/index.json` on its own, so last week's grid stays up until the new one lands. Post one line to Telegram only if the cook failed.

**How the page picks a puzzle.** It reads `puzzles/index.json` and opens the edition for the most recent Sunday if it is listed, otherwise the newest one listed. So the new week appears the moment both the JSON and its index line are pushed. Progress is stored per edition, so someone who starts on Sunday can finish on Wednesday.
