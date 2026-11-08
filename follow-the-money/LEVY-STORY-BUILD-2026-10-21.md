# Why Ohio keeps voting on school levies: build notes, October 21, 2026

Staged locally on the Issue 2 tool (`follow-the-money/index.html`). Nothing committed or pushed.

## What was added

A new spread, `section.lv` with heading id `h-levy`, placed after "What the $300.6 million plan would build" (`h-build`) and before "Lakota schools get about 56 cents" (`h-bill`). In order:

1. **Lede and the one teaching graphic.** A two-panel step chart drawn as inline SVG by `freezeChart()`. It redraws on resize, like the page's other charts. Top panel: Butler County's median home value as an index (2020 = 100, then 137 after the 2023 update and 163 after the 2026 reappraisal). Beside it, a flat line for what a voted levy collects, and a hatched gap labeled "Not collected." Bottom panel: Lakota's effective residential operating rate, 30.28 mills (TY2022), 23.29 (TY2023) and 23.25 (TY2024).
2. **Five folds, closed by default.** They sit on a numbered dated rail and run in date order: 1976 House Bill 920; 1997 to 2003 DeRolph; 2020 to 2025 pandemic relief (with the ESSER table); 2021 to 2025 House Bills 110 and 96; 2025 the veto override (with the carryover cap and Lakota's carryover marked **Unknown**). The worksheet order put the formula before the pandemic money. I swapped those two so the years run in sequence.
3. **"The 2025 budget: one override vote, two names for one school formula."** A 61-to-28 bar with its key: yes, all 61 Republicans; no, 27 Democrats and 1 Republican; 10 not recorded. Beside it, the two names, each with the documents that use it.
4. **"Where Issue 2 sits: a bond, for buildings."** Two side-by-side boxes, bond levy and operating levy. Lakota's last operating levy was in 2013, and a link points down to the forecast's 3.6-mill placeholder.
5. **Candidates, as dated quotes only.** Lakota's two House districts (45 and 46) are visible, one quote per candidate. A fold holds Districts 47, 40, 80 and 84. Each Republican incumbent also carries an "override vote: yes" line from the House Journal.
6. A sources fold for the section.

Other changes:
- 19 sources appended as **src-43 to src-61**. Existing numbers 1 to 42 are untouched; the list's numbering comes from a CSS counter, and every `id` still matches its position.
- The header now reads "Revised Oct 21, 2026". The footer revision line opens with "Posted October 2, 2026 · Revised October 21, 2026: why Ohio keeps voting on school levies, added."
- `pieces.json`, `follow-the-money` entry: `href` changed to `follow-the-money/?v=20261021` and `updated` to `2026-10-21`. `featured` was already true.

## Sources used (new numbers)

43 Ohio Revised Code 319.301 and 5705.194 · 44 LSC Members Brief, millage floors, Sept. 19, 2025 · 45 Finney Law Firm summary of the Butler County Auditor's 2023 release (37 percent; 19 percent from the Auditor's 2026 FAQ, existing src-10, which I opened and confirmed) · 46 LSC DeRolph brief, Aug. 12, 2024, and State ex rel. State v. Lewis (2003) · 47 LSC Greenbook for House Bill 96 · 48 Ohio Department of Education relief deck, April 29, 2021 · 49 to 51 Ohio Auditor of State single audits for Lakota (FY2020 to FY2025), Troy City (FY2020 to FY2025) and Talawanda (FY2020 to FY2025), each opened · 52 Troy's renewal (Dayton Daily News; Miami County election guide) · 53 Talawanda's 2022 result and the Butler County ballot list · 54 House Journal, July 21, 2025, and the House Bill 96 votes page · 55 OSBA legislative report and veto list · 56 WOSU (Senate 21 to 11) and Signal Ohio (Dec. 19, 2025 signing) · 57 the formula's two names (Hall and Gross releases; Hornbacker, Price and Childrey pages) · 58 candidates' own words, plus the Butler County Board of Elections notice and The Ballot Brief for the districts · 59 Lakota MFP funding page · 60 Ohio Capital Journal voucher figures · 61 Signal Ohio (May 2026 results) and the propertytax.report tally (131 issues).

Existing sources reused: 4, 6, 8, 10, 11, 14, 16, 17, 18, 21, 37.

## Corrections to the brief, from the record

- **Troy's ESSER did not end in fiscal 2024.** Its FY2025 audit lists another **$1,306,035** (84.425U). The page states it, and the fold never calls the FY2024 money Troy's "last."
- **Lakota's ESSER, from its state audits (new):** $597,959 (FY2020), $2,232,014, $6,047,385, $6,418,228 and $3,471,651 (FY2024). That is **$18,767,237** in all. The FY2025 audit lists none.
- **Troy's full series:** $408,456 (FY2021), $1,854,673, $2,168,028, $1,929,206 and $1,306,035, for $7,666,398. **Talawanda's:** $4,160,633 over FY2021 to FY2025, which matches the facts file.
- The table counts ESSER lines only (84.425D and U). Homeless-student lines are left out: Troy $11,500 and $15,200, Lakota $56,111 and $3,713, Talawanda $11,114. The caller's "$1,940,706" is Troy's FY2024 fund total including $11,500 for homeless students. The page says exactly that.
- **"$7.14 billion" is all federal pandemic K-12 relief to Ohio, not ESSER alone.** ESSER is $6.95 billion of it. The page says "most of it came in three rounds of ESSER."
- **"Party lines":** the 28 no votes were every Democrat recorded (27) and one Republican (Oelslager). The page says so; the phrase "party lines" is not used.
- **The 2023 value rise.** The page already said Lakota's own values rose 32.9 percent. The county median of 37 percent is a different measure. The new chart labels it "Butler County median" and uses Lakota's own mills for the rate panel.
- Rep. Rachel Baker's newsletter says "fair school funding formula," not "Fair School Funding Plan," so it is not used as an example of the name. Caleb Price's issues page is used instead.

## Left out, and why

- **"What the other side proposes"** (carryover caps, consolidation, replacement taxes, vouchers as growth). It is in the worksheet but not in today's brief, and it is a separate section. Only the carryover cap appears, in fold 5, because Lakota's carryover is the open question.
- **Hamilton County House districts (24, 27 to 30).** Which Hamilton County communities fall inside the 8th under the 2025 map is UNCONFIRMED in the research. The candidates fold is limited to the Butler, Preble, Darke and Miami seats.
- **Statewide candidates** (Ramaswamy, Acton, Husted, Brown). The brief asked for the House districts inside Ohio's 8th.
- **Policy Matters' $2.86 billion gap.** It is an advocacy group's estimate, so the page uses the LSC figures alone.
- **Lakota's carryover percentage.** Marked Unknown, as he decided. The page's own forecast data (src-4, FY25 ending cash $63.5M) could produce a number if he wants one.
- **Mullins's quote.** Her House news page has no statement on either subject. Per the rule against writing an absence into the page, her entry carries only her override vote.
- Everything tagged UNCONFIRMED in both research files, and the Journal-News's unnamed opposing argument.

## QA (headless Chrome, `scratchpad/qa-levy.cjs`, run at 390 and 1280)

- No horizontal page overflow at either width, with folds closed or open: scrollWidth equals clientWidth (390/390, 1280/1280). The only elements past the edge are the existing sample-home chips, which sit inside their own scroll strip.
- No chart text falls outside the chart at either width. An earlier label overflow at 390 was fixed.
- All 5 folds are closed on load. All 5, plus the candidates fold, open and close on a summary click.
- All 253 citations on the page resolve, 97 of them in the new spread. Clicking a new citation opens the fine print and lands on the source. The source list numbers match their ids, 1 to 61.
- Em dashes: 0 in the HTML and in the rendered text.
- The calculator still works. Typing $500,000 changes today's yearly bond tax from $280 to $399, the passes-monthly figure from $22 to $32, and taxable value to $175,000.
- No console errors.
- Fixed during QA: a class clash (`.n`) that collapsed the ESSER table's number cells; false commas between citation groups separated by text (`span.cs` breakers added); the table now uses the full width on phones; and the bars share one fixed track.
- Screenshots: `follow-the-money/shots/levy-story-390-closed.png`, `levy-story-390-open.png`, `levy-story-1280-closed.png`, `levy-story-1280-open.png`.

Pre-existing and untouched: a `#h-time` link target has no matching id on the page, and sources 26 to 35 are no longer cited after the Oct. 16 cut.

## Changed files, for a selective git add (push list)

```
follow-the-money/index.html
pieces.json            (ONE hunk only: the follow-the-money href and updated; use git add -p, the Word for Word entry is another lane's)
```

Keep out of the push: the backups (`index.before-levy-story-20261021.html`, `index.before-editor-20261021.html`), this BUILD file, `EDITOR-LEVY-2026-10-21.md`, `shots/`, the worksheet and `research/`. `follow-the-money/index.md` and `v1-dustin/index.md` were already modified before this build and are not mine.

## Still to do at push time (update-everywhere rule; not touched per today's brief)

- Landing `index.html` line 343: the static tile href still reads `follow-the-money/?v=20261016`. Bump it to `?v=20261021` so the landing matches pieces.json.
- Re-shoot `assets/previews/ftm.jpg` only if the top of the page should change; the spread sits below the fold, so the current preview is still accurate.
- Run `build-ai-twins.py` (regenerates `follow-the-money/index.md` and `llms-full.txt`, which still carries `?v=20261016`) and `add-analytics.py`.
- After the push, verify live: the page, pieces.json `updated`, and the landing's versioned link.

## Editor pass applied (October 21, 2026, after EDITOR-LEVY-2026-10-21.md)

Fresh backup first: `index.before-editor-20261021.html`.

**All seven MUST-FIX items, as the editor wrote them:**
1. The freeze is scoped to operating levies above the 20-mill floor, and the page says Lakota is above it. Changed in the lede (now cites 44, 17, 10), the fold 1 headline and summary ("about the same dollars", "effective rate"), and the fold 1 body ("each voted operating and permanent improvement levy").
2. DeRolph now reads "three times." DeRolph III (found most of the system complied; parity aid by July 1, 2003) and IV (vacated it; "unconstitutional") are split into two entries.
3. "Other vetoed items stay open to an override vote through December 31, 2026. Two of them bear on school levies": items 55 and 63, cited to 55 and 54.
4. Troy's 40.1 percent is cut, from the page and from the src-50 description.
5. Bond box: "The money can be spent only on the buildings in the plan and the debt on them."
6. Fold 5 now carries both releases as documents: the House Republican release of Oct. 1, 2025 ("ensures taxpayers have more control...") and Leader Isaacsohn's release of July 21, 2025 ("not real property tax relief"). Both are in **new src-62**.
7. Fold 4: the summary now gives 0.4 percent (FY2026) and 1.3 percent (FY2027), and the body adds the releases' "nearly $700 million more for public education over the biennium than they received in FY25" (src 57).

**SHOULD-FIX applied:** 1, "values rose by a median of," and the chart key now reads "Median value increase." 2, "effective rate," defined in place. 3, src 17 added for 1976. 4, a line on why Troy and Talawanda are in the table. 5, plain words: mill defined under the chart; emergency and substitute levies defined as fixed-sum; fiscal caution, watch and emergency defined, with **new src-63** (Auditor of State). 6, "Yes, 61: all of them Republicans." 7, the five repeated per-incumbent override-vote lines are cut, since the panel carries that fact; Mullins keeps hers because it is her only entry. 8, the as-of date (Sept. 18, one outside count) plus WVXU, Oct. 7, added to src-61. 9, item 66's 100 percent carryover bar, cited to the Gross July 22 release (src 58). 10, "held to about the dollars it first raised... until the district reaches the 20-mill floor." 11, the 2.0 permanent improvement split is dropped; the line now reads "3.5 mills, ... by 288 votes" (21, 14). 13, the fold now says "8th Congressional District" and gives its reason (the seats share Lakota's congressional seat). 14, the House Bill 33 universal EdChoice line, with Ideastream/WVXU added to src-60. 15, TY2025 23.23 mills added to the chart (src 14). 16, src 6 added to the bond-rate sentence.

**SHOULD-FIX skipped:**
- 5 (part): the replacement-levy definition and the Cupp-Patterson sponsors' names and parties. Neither has a source in hand, and the editor flagged the names as needing one.
- 12: splitting the vote-and-names panel. The brief asked for the bar "with the two names of the formula beside it," so it stays one panel.
- One thing I did not add: "rather than a set rate," which I first wrote into the levy-type definition. It was a contrast construction, and I cut it.

**Caught in QA:** a placeholder-token replacement briefly overwrote two existing `<!-- PLACEHOLDER: ... -->` comments in the "Two paths" section. Both are restored and checked identical against the backup. A diff against `index.before-levy-story-20261021.html` shows no other lines outside the spread, its CSS and JS, the sources, and the revised lines changed.

**QA re-run at 390 and 1280:**
- No page overflow, folds open or closed (390/390, 1280/1280); no chart text outside the chart.
- All 262 citations resolve, 106 in the spread. Sources 1 to 63 match their ids.
- 0 em dashes. No false commas between citation groups.
- The calculator works ($280 to $399 at $500,000). No console errors. Folds closed on load; open and close works.
- Shots replaced: `shots/levy-story-{390,1280}-{closed,open}.png`.
