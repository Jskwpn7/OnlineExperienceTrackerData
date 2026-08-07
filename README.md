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

- **Waves covered:** Wave 1 (2021) to Wave 9 (2026).
- **Wave 3 is missing — permanently.** Ofcom withdrew it after finding questionnaire errors and never republished it. There is a genuine gap in the series; trend lines skip it.
- **13+ vs 18+ break.** Waves 1–7 sampled ages **13+**; from Wave 8 the survey moved to **18+**. This matters for any youth-related reading. The tool offers two bases:
  - *As published* — each wave as Ofcom originally released it (13+ for W1–7, 18+ for W8–9). Not strictly like-for-like.
  - *18+ comparable* — the 13+ waves recomputed on an 18+ base so the series is consistent. **This 18+ recompute is our calculation, not an Ofcom-published figure** (though our per-wave 18+ bases reproduce Ofcom's published merged tables exactly).
- **Discontinuity between Waves 1–2 and Wave 4+.** The early tracker (2021–22) used an earlier survey format and sits at **markedly lower levels** than the relaunched tracker from Wave 4. For example, deepfakes "experienced" jumps from ~9% (W2) to ~18% (W4). **Treat the Wave 2 → Wave 4 step as a likely change in survey method, not a real trend.** The two periods are not strictly continuous.
- **Wave 1–2 were corrected.** Ofcom republished them in July 2023 after a tabulation error; the corrected versions are used here.
- **Question codes change across waves.** The same concept has different variable codes in different waves (e.g. scams is `q08_22` in Wave 2 but `Q8_26` in Wave 9). Items are matched by their **label text**, not code number.
- **Wave is derived from fieldwork date** in the merged file (which has no wave column). This was validated: the per-wave unweighted 18+ bases match Ofcom's published merged tables to the person.

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

- **Validation:** computed figures reproduce Ofcom's published Wave 9 data tables exactly (e.g. "very concerned about scams" 58.2%), and the per-wave 18+ bases match Ofcom's merged tables. The weighting method was also unit-tested.
- **Independence:** this is an independent analysis of Ofcom's open data. It is **not produced or endorsed by Ofcom**. Where our subgroup definitions or suppression rules differ from Ofcom's, small differences from their published tables are possible.
- **Attribution:** please credit *Ofcom, Online Experiences Tracker* as the data source. Respect Ofcom's open-data/copyright terms when sharing outputs.

## 8. Files in this project

- `OET_explorer.html` — the interactive tool (self-contained, opens offline). Includes an in-app "About & how to read" panel with the key points above.
- `estimates_long.csv` — the tidy weighted-estimates table behind the tool.
- `catalogue.csv` — index of question blocks, items, waves and base ranges.
- `oet_build_estimates.py`, `oet_backfill_w12.py`, `oet_followups.py`, `oet_followups2.py` — the reproducible data pipeline (re-run when a new wave is added).
- `build_explorer.py` + `explorer_template.html` — generate `OET_explorer.html` from the estimates (the builder injects the data into the template).
- `run_all.py` — one-command refresh: runs the whole pipeline and rebuilds the explorer.
- `PHASE0-findings.md`, `PHASE1-summary.md`, `PHASE2-summary.md`, `dashboard-additions.md` — build notes.

## 9. Updating for a new wave

Download the new wave's SAV + the refreshed merged file into `raw/`, then run **`python run_all.py`** — it chains the whole pipeline (re-derives wave from fieldwork date, crosswalks by label, recomputes the 18+ basis and effective bases) and rebuilds `OET_explorer.html`. New questions are picked up automatically.

The explorer also has, on each trend: **Chart PNG / Chart SVG** export (for slides) and **CSV** export of the current view. Exports carry their caveats with them: chart images include a title and a two-line caveat footer (basis, wave breaks, source, base), and the CSV opens with the same caveats as `#` comment lines plus a `ci95_halfwidth` column.
