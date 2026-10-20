# OET Scams & Online-Harms Explorer — README & data caveats

This explorer makes Ofcom's **Online Experiences Tracker (OET)** interactive for a defined set of topics. It is an **independent analysis built from Ofcom's published microdata — not an official Ofcom output**, and figures may differ slightly from Ofcom's published tables in edge cases. Please read the caveats below before drawing conclusions; survey data of this kind is easy to misinterpret.

## 1. What the data is

- **Source:** Ofcom Online Experiences Tracker (OET), fieldwork by YouGov. Open data published by Ofcom.
- **Method:** online panel survey, run twice a year ("waves"). ~7,000+ respondents per wave.
- **Population:** a sample designed to represent **UK internet users** (quota-controlled and weighted by age, gender, region and social grade). It does **not** represent the whole UK population — people who don't use the internet are out of scope by design.
- **Nature:** everything is **self-reported perception and experience**, collected in a ~20-minute online questionnaire. It measures what people *say* they encountered and how they *feel*, not independently verified incidence.

## 2. Scope of this tool

Deliberately narrowed to the team's topics: **scams / fraud / phishing, deepfakes (fake/deceptive images & video), impersonation / catfishing, and misinformation / fake news** (the latter included as "related content" by decision). All other harm types in the survey (hate, bullying, self-harm content, etc.) are **excluded**. The scams and misinformation detail modules (Q32) are included.

## 3. How to read the numbers

- **All percentages are survey-weighted; all bases shown are unweighted.** Weighted and unweighted figures differ — always read the % as weighted and the base as the actual number of people asked.
- **Base = who was asked.** Each question has its own base (see §6). A % is a share *of that base*, not of everyone.
- **Concern vs experience are different things.** "Concern" (Q7) is an attitude; "Experienced" (Q8) is a reported behaviour/encounter. Don't conflate them.
- **"Experienced" means the respondent believes they encountered it.** Especially for deepfakes and misinformation, this is the respondent's own judgement, which may be wrong in either direction.
- **Significance.** The trend chart shows a 95% confidence band, and each latest wave-on-wave change is flagged *sig.* / *n.s.* (a two-proportion z-test). Intervals are computed on the **Kish effective base** — `(Σw)² / Σw²` per cell — which accounts for the weighting design effect (here mild, deff ≈ 1.0–1.1). They do not add clustering or finite-population corrections, so treat them as close but not exact, and still treat small moves with caution.
- **Wave-on-wave change colouring.** The KPI delta is coloured red/green only for measures where direction is unambiguous (experienced, concern, most-recent share, money lost — a rise reads as adverse). Categorical follow-ups (actions taken, OSA knowledge, channels, etc.) show a neutral grey delta, since whether a rise is good depends on the category selected.
- **Highlights.** The Overview page auto-surfaces the biggest *significant* wave-on-wave movers and the widest subgroup gaps (base ≥100) in scope — click any highlight to jump straight to that view.
- **Charts on the trend line** mark the missing Wave 3 / Wave 2→4 method break with a dashed divider, and the line is broken there rather than drawn continuously.
- **Sharing a view.** "Copy link" (top right) encodes the current topic/measure/category/subgroup/basis in the URL, so a colleague opening the file with that link lands on the same view.

## 4. Waves, gaps and comparability (the big ones)

- **Waves covered:** Wave 1 (2021) to Wave 10 (June/July 2026).
- **Wave 3 is missing — permanently.** Ofcom withdrew it after finding questionnaire errors and never republished it. There is a genuine gap in the series; trend lines skip it.
- **13+ vs 18+ break.** Waves 1–7 sampled ages **13+**; from Wave 8 the survey moved to **18+**. This matters for any youth-related reading. The tool offers two bases:
  - *As published* — each wave as Ofcom originally released it (13+ for W1–7, 18+ for W8–10). Not strictly like-for-like.
  - *18+ comparable* — the 13+ waves recomputed on an 18+ base so the series is consistent. **This 18+ recompute is our calculation, not an Ofcom-published figure** (though our per-wave 18+ bases reproduce Ofcom's published merged tables exactly).
- **Discontinuity between Waves 1–2 and Wave 4+.** The early tracker (2021–22) used an earlier survey format and sits at **markedly lower levels** than the relaunched tracker from Wave 4. For example, deepfakes "experienced" jumps from ~9% (W2) to ~18% (W4). **Treat the Wave 2 → Wave 4 step as a likely change in survey method, not a real trend.** The two periods are not strictly continuous.
- **Wave 1–2 were corrected.** Ofcom republished them in July 2023 after a tabulation error; the corrected versions are used here.
- **Question codes change across waves.** The same concept has different variable codes in different waves (e.g. scams is `q08_22` in Wave 2 but `Q8_26` in Wave 9). Items are matched by their **label text**, not code number.
- **Wave is derived from fieldwork date** in the merged file (which has no wave column). This was validated: the per-wave unweighted 18+ bases match Ofcom's published merged tables to the person.
- **Ofcom's W4–W10 merged file is 18+ only.** From the Wave 10 release, Ofcom dropped the under-18 respondents of Waves 4–7 from the merged file (the 18+ records and their weights are otherwise identical to the W4–W9 file — checked respondent-by-respondent). The *as published* (13+) basis for W4–7 can only come from the older W4–W9 merged file, so the pipeline reads **W4–9 from the W4–W9 file and only Wave 10 from the W4–W10 file** (see `oet_sources.py`). **Keep `raw/data-sav-merged-waves-4-9.sav`** — without it the as-published W4–7 figures can't be rebuilt.

## 5. Base sizes and reliability

- **Small bases (<50) are flagged ⚠ throughout** (table, bars, KPI). Read them as *indicative at best* and don't quote them as firm.
- **Most follow-up questions are asked about a single sampled harm per respondent** — not every harm they experienced. So their bases are much smaller than the headline "experienced" numbers, and they are reliable at **Total level only**, not for fine subgroup splits. Impersonation follow-ups are frequently below 50.
- **Platform-specific questions (Q22–Q29) and the genAI-tool question (Q30) are a subset of a subset of a subset** (experienced *this* harm, on *this* channel, on *this* app). Many cells are in single digits. **They are included so the team can watch them build over future waves — they are not a basis for conclusions today.** The more usable platform views are social app (Q24), messenger (Q26) and video app (Q22).
- Subgroup breakdowns are only offered where the base supports them (concern, experience, most-recent-harm, the scams/misinformation detail, and the attitude questions). Other follow-ups are Total-only.

## 6. What each question's base is

- **Concern (Q7), Experienced (Q8):** all respondents.
- **Most recent harm (Q9):** all who experienced any harm in the last 4 weeks.
- **Scams: lost money (Q32b1):** those who experienced scams. **Type of scam money lost to (Q32b2):** those who lost money to a scam (small).
- **Misinformation type/source (Q32a/Q32a1):** those who experienced misinformation.
- **Impact, frequency, where, actions, reasons, platform, reporting (Q12–Q30):** those asked about that sampled harm.
- **Online Safety Act knowledge/confidence (Q45/Q46), own content taken down (Q34):** all respondents (Q46 also reported among those aware of the Act in Ofcom's own tables).

## 7. Provenance, validation and licensing

- **Validation:** computed figures reproduce Ofcom's published Wave 9 data tables exactly (e.g. "very concerned about scams" 58.2%) and Wave 10 data tables exactly (e.g. very concerned about scams 60.1%, experienced scams 29.0%, lost money to a scam 7.4% of 2,130; effective base 7,292 = Ofcom's ESS), and the per-wave 18+ bases match Ofcom's merged tables. Adding Wave 10 left every W1–9 figure unchanged. The weighting method was also unit-tested.
- **Independence:** this is an independent analysis of Ofcom's open data. It is **not produced or endorsed by Ofcom**. Where our subgroup definitions or suppression rules differ from Ofcom's, small differences from their published tables are possible.
- **Attribution:** please credit *Ofcom, Online Experiences Tracker* as the data source. Respect Ofcom's open-data/copyright terms when sharing outputs.

## 8. Files in this project

- `index.html` — the interactive tool (self-contained, opens offline). Includes an in-app "About & how to read" panel with the key points above.
- `estimates_long.csv` — the tidy weighted-estimates table behind the tool.
- `catalogue.csv` — index of question blocks, items, waves and base ranges.
- `oet_sources.py` — which merged microdata files feed the pipeline, and the fieldwork-month → wave map. The only file to edit for a new wave.
- `oet_build_estimates.py`, `oet_backfill_w12.py`, `oet_followups.py`, `oet_followups2.py` — the reproducible data pipeline (re-run when a new wave is added).
- `build_explorer.py` + `explorer_template.html` — generate `index.html` from the estimates (the builder injects the data into the template).
- `run_all.py` — one-command refresh: runs the whole pipeline and rebuilds `index.html`.
- `PHASE0-findings.md`, `PHASE1-summary.md`, `PHASE2-summary.md`, `dashboard-additions.md` — build notes.

## 9. Updating for a new wave

1. Download the new wave's files (SAV, data tables, technical report, questionnaire, refreshed merged file) into a new folder under `raw/` (e.g. `raw/wave 10/`).
2. In `oet_sources.py`, point `SAV_LATEST` at the new merged file and add the new wave's fieldwork months to `MONTH2WAVE` (the pipeline stops with a clear error if a month is unmapped). Leave `SAV_HIST` on the W4–W9 file.
3. Run **`python run_all.py`** — it chains the whole pipeline (re-derives wave from fieldwork date, crosswalks by label, recomputes the 18+ basis and effective bases) and rebuilds `index.html`. New response codes are picked up automatically; new *questions* need adding to the follow-up scripts.
4. Check a few headline figures against Ofcom's new single-wave data tables, and update the wave range text in `explorer_template.html` (header, About panel, export caveat) and this README.

The explorer also has, on each trend: **Chart PNG / Chart SVG** export (for slides) and **CSV** export of the current view. Exports carry their caveats with them: chart images include a title and a two-line caveat footer (basis, wave breaks, source, base), and the CSV opens with the same caveats as `#` comment lines plus a `ci95_halfwidth` column.

## 10. Wave 10 notes (added October 2026)

- **Fieldwork:** 18 June – 20 July 2026 (the data's start dates run 18 June – 18 July; §2.5 of the technical report says main fieldwork ran "7th–23rd June", which contradicts its own summary, the questionnaire and the data, so it looks like a typo). Like Wave 8, it is a **summer** wave; Wave 9 was winter (January 2026).
- **Sample:** 7,356 adults 18+ (including boosts), effective base 7,292. Weighting unchanged from Waves 8–9 (rim-weighted on age, gender, region, education and social grade; boosts included in totals, not rebalanced).
- **Questionnaire:** the technical report lists no Wave 10 changes, and the data matches: all in-scope variables, labels and response codes are unchanged from Wave 9, so no crosswalk changes were needed. Wording changed only for out-of-scope harms (self-harm, suicide, human trafficking).
- **Scam-type question (Q32b2):** the Wave 10 questionnaire shows an opt-out screen (Q32b2a) before Q32b2, so people who lost money but chose to stop there are not in the Q32b2 base. We can't tell from the files here whether this screen is new in Wave 10, but either way the base was already small.
- **Significance:** Ofcom tests wave-on-wave differences at **99%**; this tool flags them at **95%**. A change marked *sig.* here may not be called significant by Ofcom. (The two W9→W10 movers on the Overview, impersonation "very concerned" +2.7 pts and deepfakes most-recent share −2.4 pts, are significant at 99% too.)
- **Platform cells (Q22–Q29):** which harm × platform combinations have any respondents changes from wave to wave (e.g. Q&A-site cells for scams appear in W10, gaming-platform cells for scams don't). This is the expected thinness noted in §5, not a data problem.
