# Phase 2 — Interactive explorer + Q32 scams module

## The explorer — `OET_explorer.html`

A self-contained interactive tool. Double-click to open in any browser — no install, no server, works offline, shareable as a single file. Built directly on `estimates_long.csv` (all 4,512 weighted figures embedded).

What it does:
- **Pick a question** (Concern Q7 / Experienced Q8 / Scams detail Q32), **metric**, and **item**; **search** items by keyword.
- **Break down by** Gender, Age, Region, or SEG — or view the Total.
- **Trend across waves** chart (one line per subgroup), plus a **latest-wave breakdown** bar chart. With "Total" selected the breakdown compares all in-scope items side by side.
- **Basis toggle:** "18+ comparable" (waves 4–7 recomputed to 18+) vs "As published" — so the 13+/18+ break is handled visibly.
- **KPI cards:** latest value, change vs previous wave, series peak/low, and the unweighted base with a small-base warning.
- **Caveat banner** that updates with the selection, and **export** to CSV (current view) or PNG (trend chart).
- Small bases (<50) are flagged in the table, bars, and KPIs throughout.

Validated: the embedded data parses cleanly and a stubbed-DOM smoke test ran the Concern, Experienced, Gender-breakdown and Q32 scam-type views with no errors.

## Q32 scams-detail module (added)

Two new measures, both for scams specifically:
- **Lost money/assets to a scam** — % Yes among those who experienced scams. Stable ~5–7% across waves (W9 = 6.6%, base 2,148).
- **Type of scam money was lost to** — the 12 fraud types, among money-losers (small base ~140–240/wave, flagged). In Wave 9 the top types were **purchase scams (37.8%)**, impersonation fraud (19.8%) and investment/pension scams (19.1%).

These are in `estimates_long.csv` under question "Scams detail (Q32)" and selectable in the explorer.

## Waves 1–2 backfill — DONE

Added Wave 1 (2021) and Wave 2 (2022) from the SAV files you supplied. Crosswalked by **label** (codes differ — scams is `q08_22` in W1/W2 vs `Q8_26` now), mapped gender/age/region/SEG onto the modern categories, applied weights, and appended to `estimates_long.csv`. The series now runs **1, 2, 4, 5, 6, 7, 8, 9** and the explorer picks it up automatically. Q8 (experienced) is present for both waves; the Q7 concern grid exists in Wave 1 only (Wave 2 didn't field it), and there's no Q32 scams module that far back. Waves 1–2 are 13+, so they also get an 18+ recompute for the comparable basis.

**Important caveat surfaced:** waves 1–2 sit at much lower levels than waves 4+ (e.g. deepfakes experienced 8.8% in W2 vs 18% in W4; misinformation 23%→39%). This jump across the 2→4 step looks like a **survey-format change at the relaunch**, not a real trend — the early tracker and the relaunched (wave 4+) tracker aren't strictly continuous. The explorer footer now flags this, and the qualitative pattern checks out (Ofcom's W1–2 summary report says scams was the most-experienced harm, which matches our W1/W2 figures).

## Files (Phase 2)

`OET_explorer.html` (the tool) · updated `estimates_long.csv` & `catalogue.csv` (now incl. Q32) · `build_explorer.py` & `oet_build_estimates.py` (reproducible builders).

## Status

Phases 0–2 complete, including both add-ons (Q32 scams module and the waves 1–2 backfill). The data layer is validated against Ofcom's published figures and the explorer covers the full 2021–2026 series. Optional future polish: significance markers on wave-on-wave changes, and a "what changed most" auto-highlight.
