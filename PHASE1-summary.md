# Phase 1 — Catalogue + weighted estimates (waves 4–9)

Built the analysable dataset that the explorer will sit on top of: a question catalogue and a tidy weighted-estimates table covering the in-scope topics across the modern series (waves 4–9), with the 18+ comparability recompute and small-base flags. All from the merged microdata you downloaded.

## What was built

- **`catalogue.csv`** — the in-scope items mapped to their variables and the waves they appear in (concern `Q7_*` and experienced `Q8_*`, for scams, deepfakes, catfishing, misinformation).
- **`estimates_long.csv`** — 4,032 rows of weighted estimates. One row per: wave × metric × item × subgroup × subgroup-value × basis, with `weighted_pct`, `unweighted_base`, and a `small_base` flag (<50).
  - metrics: `very_concerned` (top box), `any_concern` (codes 1–5), `experienced` (yes)
  - subgroups: All, Gender, Age, Region, SEG (AB / C1C2 / DE)
  - basis: `as_published` (each wave as originally released — 13+ for W4–7, 18+ for W8–9) **and** `age18plus` (18+ throughout, for a like-for-like trend)
- **`trend_experienced_18plus.png`** — quick trend chart of harms experienced (18+ basis).
- **`oet_build_estimates.py`** — the reproducible build script (re-runs when a new wave is added).

## How the data was wrangled (two findings worth knowing)

1. **There is no wave column in the merged file.** Wave is derived from the fieldwork date (`starttime`): the 52,429 records fall into six clean date clusters = waves 4–9. This is validated below.
2. **The merged published tables are reported 18+ throughout**, even though waves 4–7 were originally 13+. The merged file still contains the 13–17s for W4–7 (976/543/557/588 of them), so both bases are reproducible.

## Validation — the numbers are correct

- **Wave 9 "very concerned" matches Ofcom's published tables exactly** for all four in-scope items: scams 58.2%, deepfakes 53.0%, catfishing 41.2%, misinformation 49.0%.
- **Per-wave 18+ unweighted bases match Ofcom's merged tables exactly:** W4 13,205 · W5 7,068 · W6 7,280 · W7 7,378 · W8 7,340 · W9 7,494 (total 49,765). This confirms both the date→wave derivation and the 18+ filter.
- **Internal consistency:** for W8 and W9 (already 18+) the `as_published` and `age18plus` figures are identical, as they must be.
- Weights are normalised per wave (each wave's weights sum to its n), so per-wave percentages are correct.

## What the data already shows (18+ comparable basis)

% who **experienced** each harm online in the last 4 weeks:

| Item | W4 | W5 | W6 | W7 | W8 | W9 |
|---|---|---|---|---|---|---|
| Deepfakes | 18.2 | 16.1 | 18.2 | 20.9 | 22.0 | **24.5** |
| Misinformation / fake news | 39.3 | 37.0 | 39.2 | 42.1 | 41.3 | 41.6 |
| Scams, fraud, phishing | 35.8 | 34.2 | 33.9 | 34.2 | 33.7 | **28.6** |
| Catfishing / impersonation | 10.1 | 10.4 | 11.5 | 11.3 | 9.2 | 8.6 |

Notable for the team:
- **Deepfakes show a clear, sustained rise** — 18% → 24.5% since 2023, the only steadily climbing harm.
- **Scams experience dropped in Wave 9** (≈34% → 28.6%) after being flat for years — worth a closer look at what changed.
- Misinformation is consistently the most-encountered (~40%); catfishing is low and edging down.
- The 13+ vs 18+ choice moves W4–7 figures by only ~1 point (e.g. scams W4 35.8% on 18+ vs 35.0% as-published), so the long trend is robust to that break.
- Wave 9 scams experience is fairly flat across age groups (26–32%), i.e. not a young-person-specific issue.

## Files

`catalogue.csv` · `estimates_long.csv` · `trend_experienced_18plus.png` · `oet_build_estimates.py`

## Next steps

- **Backfill waves 1–2** (different variable names — label-based crosswalk) to extend the series back to 2021, if the team wants the longer history.
- **Phase 2 — the explorer:** build the Streamlit (or static) front-end on `estimates_long.csv`: search the catalogue, pick an item, break by subgroup, view the trend with the 13+/18+ toggle and the Wave-3 gap annotated, chart and export. The data layer is now ready for it.
- Optionally add the **`Q32` scams module** (impact, amount lost, fraud type) — richer but only asked of those who experienced scams, so it needs its own base handling.
