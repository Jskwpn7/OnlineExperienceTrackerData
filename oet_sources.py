"""Single place that defines which merged microdata files feed the pipeline,
and how fieldwork months map to waves.

Why two files?  From the W4-W10 release Ofcom's merged file is **18+ only** --
the under-18 respondents of Waves 4-7 were dropped (all 18+ records and their
weights are otherwise identical to the W4-W9 file; checked respondent-by-
respondent on caseid). The "as published" (13+) basis for W4-7 can therefore
only be computed from the older W4-W9 merged file. So:

  * SAV_HIST   -- the last merged file that still contains the 13+ records
                  (W4-W9). Used for every wave it covers. Do not replace.
  * SAV_LATEST -- the newest merged file Ofcom has published. Only records from
                  fieldwork months NOT already in SAV_HIST are taken from it
                  (i.e. the new wave(s)).

For a new wave: download the new merged file, point SAV_LATEST at it, add the
new fieldwork months to MONTH2WAVE, then run `python run_all.py`.
"""
import pandas as pd, pyreadstat

SAV_HIST = "raw/data-sav-merged-waves-4-9.sav"
SAV_LATEST = "raw/wave 10/data-sav-merged-waves-4-10.sav"

MONTH2WAVE = {"2023-07": 4, "2024-01": 5, "2024-05": 6, "2024-06": 6, "2025-01": 7,
              "2025-06": 8, "2025-07": 8, "2026-01": 9,
              "2026-06": 10, "2026-07": 10}   # W10: fieldwork 18 Jun-20 Jul 2026 (data: 18 Jun-18 Jul)


def _month(df):
    return pd.to_datetime(df["starttime"], errors="coerce").dt.to_period("M").astype(str)


def read_merged(usecols):
    """Return (df, meta) combining SAV_HIST with the new-wave records of SAV_LATEST.
    meta.variable_value_labels is the union of both files' value labels (latest
    wins on a clash -- none exist for the variables used as of W10)."""
    usecols = list(dict.fromkeys(usecols))
    h, mh = pyreadstat.read_sav(SAV_HIST, usecols=usecols)
    l, ml = pyreadstat.read_sav(SAV_LATEST, usecols=usecols)
    hist_months = set(_month(h))
    l = l[~_month(l).isin(hist_months)]
    df = pd.concat([h, l], ignore_index=True)
    vvl = {}
    for k in set(mh.variable_value_labels) | set(ml.variable_value_labels):
        vvl[k] = {**mh.variable_value_labels.get(k, {}), **ml.variable_value_labels.get(k, {})}
    ml.variable_value_labels = vvl
    return df, ml
