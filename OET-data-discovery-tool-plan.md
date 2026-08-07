# OET Data Discovery Tool — Plan

A tool to make Ofcom's **Online Experiences Tracker (OET)** survey results interactive and analyseable: search the question bank, filter and crosstab by subgroup, track results across waves, chart any selection, and export.

Source data: Ofcom OET publications, https://www.ofcom.org.uk/media-use-and-attitudes/online-habits/internet-users-experience-of-harm-online

**Audience & scope (decided):** internal use by a policy team that specialises in this area, for open-ended exploration — spotting trends and anything notable in the data, not producing fixed published outputs. **Topic scope is deliberately narrow: scams, fraud, deepfakes and related content** (e.g. impersonation, fake/misleading content, financial/romance scams). All other harm types (bullying, hateful content, self-harm content, etc.) are **out of scope** and should be excluded from the question bank rather than just hidden — this keeps the dataset small and the tool focused.

---

## 1. What the OET actually publishes (and what we can build on)

The OET is a twice-yearly online survey of 7,000+ UK internet users on attitudes to and experiences of online services, including potential online harms (~50+ questions, 40+ harm types). Waves to date: Wave 1 (2021) through **Wave 9 (Apr 2026)**. Note two important wrinkles:

- **Wave 3 was withdrawn** by Ofcom (questionnaire errors affecting harm measures) and never republished — there is a gap in the series.
- **Methodology break at Wave 8 (2025):** sample age range changed from **13+ to 18+**. Pre-Wave 8 and Wave 8+ figures are not strictly like-for-like, especially anything involving young people.

For each wave Ofcom releases several artefacts. Which one we ingest is the single most important design decision:

| Artefact | Format | What it is | Fit for the tool |
|---|---|---|---|
| **Data tables** | XLSX (30–60 MB) | Pre-computed crosstabs: question × subgroup, weighted %, base sizes | Easy stats, but messy merged-cell layout and limited to crosstabs Ofcom chose |
| **Microdata** | SPSS `.sav` (also CSV for W1–2) | Respondent-level rows, one per person, with survey weights | **The real "analyseable" source** — any crosstab, any filter, custom recodes, significance tests |
| **Codebook / Map / Label** | XLSX | Variable → question text → answer-code → label mappings | Needed to turn cryptic variable names into a human question bank |
| Questionnaire / Data guide | PDF | Full wording, routing, definitions | Reference + tooltips |
| Technical report | PDF | Weighting, base sizes, sampling error | Methodology notes, caveats |

Crucially, Ofcom also publishes **merged microdata for waves 4–9** (`.sav`, plus SPSS codebook/labels), which is the cleanest foundation for trend analysis across the modern series.

**Recommendation:** build on the **merged waves 4–9 microdata** as the spine (consistent, modern), and **also ingest waves 1–2** from their separate CSV/SAV releases to maximise the time series. Use the codebook/map/label files to construct the question bank, and use the pre-computed XLSX data tables as a *validation cross-check* (confirm our weighted % matches Ofcom's published %). Every wave carries comparability metadata (see §10) so the older 13+ waves can be shown, caveated, or filtered out as the user chooses. Wave 3 is permanently absent.

---

## 2. Goals and non-goals

**Goals**
- Let the team find any *in-scope* (scam/fraud/deepfake-related) OET question by keyword/topic without knowing variable names.
- Produce a weighted estimate for any in-scope question, broken by standard subgroups (age, gender, region, nation, SEG).
- Compare a metric across waves as a trend, with the Wave 3 gap and the 13+/18+ break clearly flagged — trend-spotting is the team's primary use.
- Auto-chart every selection and export results (CSV + image) and a shareable link.
- Always show the unweighted base and grey out / warn on small bases.
- Surface "anything interesting": e.g. flag the largest wave-on-wave moves and the biggest subgroup gaps within scope, so the team has a starting point rather than a blank canvas.

**Non-goals (at least initially)**
- **Harm types outside scams/fraud/deepfakes** — excluded from ingestion entirely.
- Re-deriving Ofcom's published headline figures to the decimal in every edge case (we validate against their tables, but their exact subgroup definitions/suppression rules may differ).
- Modelling / regression / inferential causal work — this is descriptive exploration.
- Polished public/published outputs — this is an internal exploration tool.
- Ingesting other Ofcom trackers (Technology Tracker, Media Use & Attitudes, Online Nation). Keep architecture generic enough to add them later, but scope v1 to OET only.

---

## 3. Data model

Two layers.

**(a) Catalogue (metadata), built from codebook/map/label:**
- `variables`: variable_id, question_id, question_text, response options + labels, type (single/multi/scale), topic tags, which waves it appears in.
- `subgroups`: the demographic/breakdown variables and their categories.
- `waves`: wave number, fieldwork dates, age base (13+/18+), sample size, status (live/withdrawn), and **comparability flags** (see §10) — e.g. `age_base`, `series_break`, `data_quality_note`, source file format (CSV vs merged SAV).

This catalogue powers search and the "what can I break this by?" UI, and records *comparability* (which questions are consistent across which waves) so the tool can caveat or filter automatically.

**(b) Estimates.** Two viable strategies:

- **On-the-fly (server):** keep respondent-level microdata in a columnar store (DuckDB/Parquet) and compute weighted % + base + (optionally) confidence intervals per request. Maximum flexibility; needs a small backend.
- **Pre-computed (static):** offline, generate a tidy **long table** of weighted estimates for every question × every standard subgroup × every wave — columns like `wave, variable_id, response, subgroup_var, subgroup_value, weighted_pct, unweighted_base, ci_low, ci_high`. Ship as Parquet/JSON. The front-end just filters this. No live backend; trivially publishable.

For a discovery tool the **pre-computed long table is the sweet spot**, and since custom crosstabs are explicitly out of scope (decision 3), it's the chosen approach for v1: it's fast, the heavy survey-weighting logic runs once in a reviewed pipeline rather than live, and the data volume is tiny once filtered to the in-scope topics and standard subgroups. The on-the-fly engine is dropped from scope.

---

## 4. Pipeline (offline, run once per new wave)

1. **Download** every available wave's microdata into the project folder: merged waves 4–9 (`.sav`) plus the standalone waves 1–2 (CSV/SAV), with their codebook/map/label + data tables. Keep the source `?v=` versioned URLs for provenance. (Wave 3 is unavailable.)
2. **Read microdata** with `pyreadstat` (reads SPSS `.sav` with value labels and weights intact).
3. **Harmonise** variable names across waves (they drift); build a crosswalk so the same concept lines up wave to wave. Flag non-comparable items.
4. **Build the catalogue** from codebook/map/label → the metadata tables above.
5. **Compute weighted estimates** applying the survey weight, for each question × standard subgroup × wave, with unweighted base and CIs. Suppress/flag bases below a threshold (e.g. <50).
6. **Validate** a sample of computed figures against the published XLSX data tables; log discrepancies.
7. **Export** the tidy long table + catalogue as Parquet/JSON for the app.

This pipeline is the bulk of the real work; the UI is comparatively cheap once the data is tidy.

---

## 5. Features (priority order)

1. **Question-bank search** — keyword/topic search over question text + tags; shows which waves each question covers.
2. **Result view** — pick a question → weighted distribution for the latest wave, with base size.
3. **Subgroup breakdown** — break the selected question by one subgroup (age, gender, nation/region, SEG…); side-by-side bars.
4. **Trend over waves** — line chart of a chosen response across waves, with the Wave 3 gap and 13+/18+ break annotated.
5. **Charts + export** — auto chart per selection; export CSV and PNG/SVG.
6. **Shareable state** — encode current selection in the URL so a view can be linked.
7. **Base-size & significance flags** — grey out small bases; optionally mark wave-on-wave changes that exceed sampling error.

Nice-to-later: saved views, downloadable methodology notes per chart. (Cross-question filtering — "among people who experienced X, what do they think about Y" — is out of scope per decision 3, as it would need a live engine.)

---

## 6. Architecture options

| Option | Stack | Best when | Trade-off |
|---|---|---|---|
| **A. Static + browser** (recommended v1) | Pipeline → Parquet/JSON → static site (vanilla JS or React) with DuckDB-WASM or pre-loaded JSON; charts via Chart.js/Plotly | Audience is broad / publishable; no infra to run | Limited to pre-computed standard crosstabs |
| **B. Analyst app** | Python pipeline → DuckDB → Streamlit | Internal analysts who want quick iteration | Needs to be run/hosted; less polished UX |
| **C. Full web app** | Pipeline → API (FastAPI + DuckDB) → React | Public tool needing arbitrary custom crosstabs at scale | Most build + hosting effort |

Recommendation given the audience: **Option B (Streamlit analyst app)** is the strongest v1 — internal policy specialists doing open-ended exploration value quick, flexible iteration over the standard subgroups, and Streamlit is the least effort for that. With custom crosstabs out of scope, both A and B run off the same pre-computed estimates, so **Option A (static, single shareable link, nothing to host)** is an equally clean alternative if you'd rather not run an app. Pick based on distribution preference; the pipeline is identical either way.

---

## 7. Phased build

- **Phase 0 — Spike (½–1 day):** download Wave 9 `.sav` + codebook, read it with `pyreadstat`, reproduce one published figure with weights applied. Confirms the whole approach end-to-end.
- **Phase 1 — Pipeline + catalogue:** ingest the full series (merged waves 4–9 plus standalone waves 1–2), filter to the in-scope topics, build the catalogue and the tidy estimates table for standard subgroups (with the 18+ recompute for older waves); validate against XLSX tables.
- **Phase 2 — Explorer v1:** search → result → subgroup breakdown → trend → charts → export, with wave-range / base toggle / comparable-waves controls. Ship Option A or B.
- **Phase 3 — Polish:** base-size/significance flags, "what's interesting" highlights (biggest moves & gaps), shareable views, methodology tooltips.
- **Phase 4 (optional):** add other Ofcom trackers using the same pattern.

---

## 8. Key risks / things to get right

- **Survey weights are mandatory.** Unweighted percentages will be wrong and won't match Ofcom. Validate against published tables early (Phase 0).
- **The 13+ → 18+ break and the missing Wave 3** must be visible in every trend, or the tool will mislead. Bake comparability flags into the data model, not just the UI.
- **Variable names drift across waves** — the crosswalk is fiddly and is where most pipeline effort goes.
- **Small base sizes** in subgroup cells must be suppressed/flagged to avoid over-interpretation.
- **Messy XLSX tables** (merged cells, multi-row headers) make them poor as a primary source — another reason to prefer microdata.
- **Licensing:** OET data is published under Ofcom's copyright/re-use terms; a published tool should attribute Ofcom and link the source. Worth confirming the re-use licence before publishing externally.
- **File sizes:** merged microdata is large (100s of MB). Keep raw files out of any published bundle; ship only the compact pre-computed estimates.

---

## 9. Decisions

1. ~~**Audience**~~ — **Decided:** internal policy team, exploratory, scoped to scams/fraud/deepfakes. Leans to Option B (Streamlit analyst app).
2. ~~**Wave coverage**~~ — **Decided:** ingest **as much of the series as possible** (waves 1–9, minus withdrawn Wave 3) because the long time series is of interest. Manage the data-quality/comparability issues via caveats and filtering rather than by dropping waves — see §10.
3. ~~**Custom crosstabs**~~ — **Decided:** the **standard subgroup set is enough** (age, gender, nation/region, SEG). No arbitrary "filter by any question" analysis needed for v1. This lets us use the simpler **pre-computed estimates** approach and drop the live on-the-fly engine from scope.
4. **Build vs. plan** — do you want me to run Phase 0 now (download Wave 9, prove the weighted-figure approach, and stand up a small prototype), or refine this plan first?

### Open question raised by the scope decision
- **Defining "in scope" precisely.** Before ingestion I'll need to identify exactly which OET questions count as scams/fraud/deepfakes/related. The OET questionnaire/codebook lists each harm type, so I can pull the candidate list and have you confirm the include/exclude boundary (e.g. is "fake/misleading information" in or out? "impersonation"? "romance scams"?). This becomes a small, reviewable scope list that drives the pipeline filter.

---

## 10. Handling the full series: comparability & data quality

Because we're keeping every available wave, the tool must make the known issues visible and manageable rather than silently averaging over them. The approach:

- **Wave 3 gap.** Permanently withdrawn by Ofcom (questionnaire errors). Trends skip it; charts annotate the break so the line isn't read as continuous.
- **13+ → 18+ break at Wave 8.** Waves 1–7 sample 13+, waves 8–9 sample 18+. This is the biggest comparability risk for a scams/deepfakes audience if under-18s behave differently. Mitigations, in order of preference:
  - Default the trend view to a **consistent 18+ base across all waves** where the microdata allows recomputing earlier waves filtered to 18+ (the microdata makes this possible — a key advantage of building on `.sav` rather than the pre-tabulated tables).
  - Offer a toggle: "as published (13+ then 18+)" vs "18+ throughout (recomputed)".
  - Where a consistent base isn't possible, draw the pre/post-break segments in distinct styles with a caveat.
- **Waves 1–2 corrections.** Ofcom republished W1–2 (July 2023) after a Q7 tabulation error; use only the corrected files and record that in provenance.
- **Question/variable drift.** Not every in-scope question exists in every wave, and wording can change. The catalogue records, per question, exactly which waves it's comparable across; trends only plot waves where the item is genuinely like-for-like, and flag wording changes.
- **Filtering to accommodate, per your steer.** The UI exposes these as controls: a wave range selector, the 13+/18+ base toggle, and a "comparable waves only" switch. Every chart shows a short auto-generated caveat line (base, waves included, any breaks) and carries it into exports so a chart can't travel without its caveat.
- **Data model support.** All of the above is driven by the `waves` comparability flags and per-question wave-availability in the catalogue (§3) — the logic lives in data, so caveats are consistent everywhere and easy to update when Wave 10 lands.
