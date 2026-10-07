# AI Gauges

> Your own AI use, on the dash: tokens, energy, water and carbon. Free, from DNSC.

Power needs gauges · v0.6

## AI Gauges

Your own AI use, read like a car's dashboard: energy, output speed, water, cache, carbon. You are looking at a sample day until you bring your own.

Energy today

output tokens

Water today

Cache hit share

Carbon today

### Reading the gauges

every estimate shows its formula and inputs

**See it with your own numbers three ways in · nothing leaves this browser**

A file picker.

A file picker (.json,.jsonl,.ndjson,.txt,.zip).

Buttons: Open my Claude Code folder, Open a file, Load the sample.

Files are read in your browser only; nothing leaves this page.

### Load your own

three ways in · pick the one you use · nothing leaves this browser

1Claude Code exact counts

1. Claude Code already keeps a log of every session on your computer: one `.jsonl` file per session, inside `~/.claude/projects`.
2. Click **Open my Claude Code folder** above.
3. That folder is hidden. On a Mac, in the window that opens press Cmd Shift G (Go to Folder), type `~/.claude/projects`, press Return. The same shortcut works in Finder, under Go, then Go to Folder.
4. Choose the `projects` folder. Your browser may say "upload"; the files are read on this page and never sent anywhere.
5. Windows: the folder is `%USERPROFILE%\.claude\projects`. Paste that into the picker's address bar.

Gives real token counts, cache included.

2Claude.ai, web or app estimate

1. In Claude, open **Settings**, then **Privacy**, then **Export data**.
2. An email arrives with a link to a `.zip` file. Download it.
3. Double-click the zip to unzip it. Inside is `conversations.json`.
4. Drop `conversations.json` anywhere on this page, or click **Open a file** and pick it.

The export has the text of your chats but no token counts, so tokens are estimated from text length: characters ÷ 4. No cache data in this export.

3ChatGPT estimate

1. In ChatGPT, open **Settings**, then **Data controls**, then **Export data**, and confirm.
2. An email arrives with a link to a `.zip` file. Download it.
3. Double-click the zip to unzip it. Inside is `conversations.json` (you can ignore the other files).
4. Drop `conversations.json` anywhere on this page, or click **Open a file** and pick it.

Same as Claude.ai: text only, so tokens are estimated as characters ÷ 4. No cache data in this export.

Drop a `projects` folder or a `conversations.json` here, or anywhere on the page. Another agent or a local model can write a usage log instead: one JSON line per turn with `ts` and `output_tokens` (the USAGE-LOG-FORMAT.md spec). Open it with **Open a file**.

### Today and this month

A choice (Unit): tokens, Wh, API $.

Estimated energy today, Wh, cloud tokens vs this Mac

Every token Claude Code counts is cloud compute: the model runs in a data center, your Mac only sends and receives text. The API carries an `inference_geo` field for where it ran; in these logs it reads "not_available," so the places below are the public record, not a measurement.

### The month's draw

estimates · edit the recipe card below

### What this water means

the record

**Which water.** Two different waters are on the meter. The first is used at the data center to cool the racks; the second is used at the power plant to make the electricity. The power plant share is usually the bigger one, and it is the one most public per-query numbers leave out.

**Consumed, not withdrawn.** The meter counts water that evaporates and does not return to the basin. Cooling towers consume 50 to 80% of what they withdraw; once-through cooling returns almost all of it, warmer; closed-loop chip cooling consumes close to none but shifts load to electricity. Withdrawal figures would be larger, and most of that water goes back.

**What the companies publish.** Google: a median Gemini text prompt uses 0.26 mL of water at the data center, about five drops, power plant water excluded. Microsoft: fleet cooling intensity 0.27 liters per kWh in 2025, and it reports replenishing more water than it withdraws. Sam Altman: about one fifteenth of a teaspoon per ChatGPT query; his later "38,000 queries per almond" line was fact-checked as overstated. Anthropic has published no water figure, so this page estimates from the others.

**Where it happens matters.** A liter evaporated in a water-stressed basin competes with farms and taps; the same liter in a wet region often does not. Roughly two in five US data centers sit in high water-stress areas. The places on this page are on the public record; the API does not say where a given request ran.

**How to read your number.** A single message is a few drops. A month of heavy work is a few showers. Both are true, and the gauge shows both so neither side gets to win the argument by picking a unit.

### Where the heat comes from

the supply chain behind the gauges

### The recipe card

every estimate on this page comes from these numbers

### Bring your own kitchen

share this page with anyone

Anyone can read their own gauges here. The three ways in are at the top under Load your own. Everything is read in your browser and drawn here. Nothing is uploaded.

Buttons: Open my Claude Code folder, Open a file.

Mise · v0.6 · measured means read from your logs; estimates carry a band and a source

---

Source: https://tools.dnsc.ai/ai-gauges/ · Generated from the page on Oct 7, 2026
