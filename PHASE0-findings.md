# Phase 0 — Findings

Goal: prove the build approach end-to-end before committing to the full tool. Three things to establish — (1) which questions are in scope, (2) can we get and read the microdata, (3) does a weighted figure computed from microdata match Ofcom's published figure.

## 1. In-scope questions — DONE

Read the Wave 9 questionnaire. The scam/fraud/deepfake content sits in two places:

- **The harm-type grids** used by several questions, where four items are in scope:
  - Item 26 — *Scams, fraud, or phishing* (core)
  - Item 24 — *Fake or deceptive images/videos, e.g. "deep fakes"* (core)
  - Item 19 — *People pretending to be another person, e.g. catfishing* (related — impersonation)
  - Item 11 — *Misinformation / false or misleading stories e.g. "fake news"* (**boundary — please confirm in/out**)

  These grids appear as **Q7 (how concerned you are)** and **Q8 (seen/experienced in the last 4 weeks)**, plus their impact/response follow-ups.
- **A dedicated scams/fraud module**: **Q32b** (what happened as a result, including losing money/assets) and **Q32b2** (which of 12 online fraud/scam types you lost money to — impersonation fraud, investment scam, romance scam, purchase scam, identity fraud, etc.).

Full list with variable examples is in `in_scope_questions.csv`. **One decision for you:** is *misinformation / fake news* in scope as "related content", or out? It's the only ambiguous item.

## 2. Getting and reading the data — DONE

- **Reading works.** You downloaded the 2026 (Wave 9) files into `raw/`, including `data-sav-wave-9-only.sav` (7,494 respondents, 3,882 columns) and the merged waves 4–9 SAV/tables. `pyreadstat` reads the SPSS `.sav` with labels and the survey weight intact. Confirmed `weight` exists and sums to 7,494 (normalised to sample size).
- **In-scope variables located in the real data.** Wave 9 uses uppercase names: concern = `Q7_26` scams, `Q7_24` deepfakes, `Q7_19` catfishing, `Q7_11` misinformation; experienced-in-last-4-weeks = `Q8_26 / Q8_24 / Q8_19 / Q8_11`; plus the `Q32*` scams module (29 variables). `Q8_*` items are coded 0=No, 1=Yes. Subgroups present: `D1_C8` gender, `D3` region, `D2_*` age bands, ethnicity/nation/disability nets, etc.
- **Comparability finding confirmed.** The harm-item **code numbers change between waves**. "Scams/fraud/phishing" is `Q8_26` in Wave 9 but `q08_22` in Wave 2 (deepfakes `Q8_24` vs `q08_20`, etc.). **The cross-wave crosswalk must match on label text, not number.** The pipeline does this.
- **One acquisition note for the pipeline:** these files can't be pulled programmatically in this environment (no sandbox network; the fetch tool caps at ~70 KB). The workflow is "download the wave files, drop them in `raw/`, run the script" — which is exactly what we just did.

## 3. Weighted figure vs published — VALIDATED ✓

Computed weighted figures directly from the Wave 9 microdata and compared to Ofcom's published `data-tables-wave-9-only.xlsx` (sheet "Q7. Online harms concern"). **% "very concerned" (code 5), base = all 7,494 respondents:**

| Item | My figure (from microdata) | Ofcom published | Match |
|---|---|---|---|
| Scams, fraud, phishing | 58.2% | 58.2% | ✓ exact |
| Fake/deceptive images (deepfakes) | 53.0% | 53.0% | ✓ exact |
| Catfishing / impersonation | 41.2% | 41.2% | ✓ exact |
| Misinformation / fake news | 49.0% | 49.0% | ✓ exact |

All four reproduce Ofcom's published numbers exactly — the weighting and reading approach is correct.

For reference, the **experienced in the last 4 weeks (Q8)** weighted prevalence from the same file: scams/fraud **28.6%**, deepfakes **24.5%**, catfishing **8.6%**, misinformation **41.6%**; and scams experienced by gender: men **32.7%**, women **24.5%** — an early example of the kind of subgroup gap the tool will surface.

The pipeline's weighting maths was also separately unit-tested on a known-answer synthetic dataset (weighted 60.0% vs unweighted 50.0%) to prove the logic in isolation.

## Deliverables from Phase 0

- `oet_pipeline.py` — working, unit-tested pipeline (read → in-scope filter → weighted estimates by subgroup → tidy CSV).
- `in_scope_questions.csv` — the candidate in-scope question list.
- `q9.txt` — extracted Wave 9 questionnaire text (reference).

## What this tells us about the plan

- The approach is sound: microdata is readable, weighting is correct, in-scope filtering works, and the cross-wave label-crosswalk requirement is confirmed (and handled).
- The only real friction is **data acquisition** — these files must be downloaded manually and placed in the folder; they can't be pulled programmatically here. Worth noting for the pipeline: it'll be a "drop the wave files in, run the script" workflow rather than an automatic fetch.

## Next steps

1. You: confirm the misinformation/fake-news boundary (in scope as "related content", or out?).
2. Me: proceed to Phase 1 — ingest the full series (Wave 9 + merged waves 4–9, then backfill 1–2), build the question catalogue and the tidy weighted-estimates table for all in-scope items × standard subgroups × waves, with the 18+ recompute and comparability flags. Validation approach is now proven, so this is mechanical.
