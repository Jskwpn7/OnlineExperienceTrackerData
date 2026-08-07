"""
OET Data Discovery Tool — Phase 0 pipeline (prototype)

Reads an Ofcom Online Experiences Tracker microdata file (SPSS .sav or CSV),
filters to the in-scope topics (scams / fraud / deepfakes / related), applies
the survey weight, and produces a tidy long table of weighted estimates by
standard subgroup. Designed so its numbers can be checked against Ofcom's
published data tables.

Usage:
    python oet_pipeline.py path/to/microdata.sav --wave 9 --out estimates_w9.csv

Notes
-----
* The harm-item code numbers DIFFER across waves (e.g. "scams/fraud/phishing"
  is item 26 in the Wave 9 questionnaire but variable q08_22 in Wave 2), so the
  in-scope match is done on the variable LABEL, never the code number.
* Percentages MUST be weighted (column `weight`) or they will not match Ofcom.
* Small unweighted bases are flagged (default threshold 50).
"""
from __future__ import annotations
import argparse
import re
import sys
import pandas as pd

# --- In-scope topic definition -------------------------------------------------
# Match on the question/answer LABEL text. Tune this list with the policy team.
IN_SCOPE_PATTERNS = [
    r"scam", r"fraud", r"phish",
    r"deep[\s-]?fake", r"deceptive image", r"fake or deceptive",
    r"catfish", r"pretending to be another person", r"impersonat",
    r"misinformation", r"fake news", r"false or misleading",
]
IN_SCOPE_RE = re.compile("|".join(IN_SCOPE_PATTERNS), re.IGNORECASE)

# Standard subgroup variables (OET naming; adjust per wave via the codebook).
SUBGROUP_VARS = {
    "d01": "Gender",
    "d02": "Age",
    "d03": "Region",
    "d04b": "Social grade (SEG)",
}
WEIGHT_VAR = "weight"
SMALL_BASE = 50


def read_microdata(path: str):
    """Return (df, meta). meta.column_names_to_labels maps var -> label."""
    if path.lower().endswith(".sav"):
        import pyreadstat
        df, meta = pyreadstat.read_sav(path)
        labels = dict(meta.column_names_to_labels)
        return df, labels
    # CSV fallback (waves 1-2). Labels unknown from data alone; caller may pass a
    # variables CSV. Here we use column names as labels.
    df = pd.read_csv(path)
    return df, {c: c for c in df.columns}


def find_in_scope_vars(labels: dict[str, str]) -> dict[str, str]:
    """Variables whose label matches an in-scope pattern, excluding subgroup/admin."""
    out = {}
    for var, lab in labels.items():
        if var in SUBGROUP_VARS or var == WEIGHT_VAR:
            continue
        if lab and IN_SCOPE_RE.search(str(lab)):
            out[var] = lab
    return out


def weighted_pct(df: pd.DataFrame, var: str, weight: str,
                 positive_values=(1,)) -> tuple[float, float]:
    """Weighted % of respondents with a 'positive' answer, plus unweighted base.

    For OET multi-select 'experienced/concerned' items, 1 = selected. Rows where
    the item is missing are treated as not-asked and excluded from the base.
    """
    s = df[[var, weight]].dropna(subset=[var])
    base_n = len(s)
    if base_n == 0:
        return float("nan"), 0
    w = s[weight].astype(float)
    pos = s[var].isin(positive_values).astype(float)
    pct = 100.0 * (pos * w).sum() / w.sum()
    return round(pct, 1), base_n


def build_estimates(df, labels, wave: int) -> pd.DataFrame:
    if WEIGHT_VAR not in df.columns:
        raise SystemExit(f"Weight column '{WEIGHT_VAR}' not found — cannot weight.")
    scope = find_in_scope_vars(labels)
    if not scope:
        raise SystemExit("No in-scope variables matched — check labels/patterns.")
    rows = []
    for var, lab in scope.items():
        # Overall
        pct, base = weighted_pct(df, var, WEIGHT_VAR)
        rows.append(dict(wave=wave, variable=var, label=lab,
                         subgroup_var="ALL", subgroup_value="All respondents",
                         weighted_pct=pct, unweighted_base=base,
                         small_base=base < SMALL_BASE))
        # By each subgroup
        for sv, sname in SUBGROUP_VARS.items():
            if sv not in df.columns:
                continue
            for val, g in df.groupby(sv):
                pct, base = weighted_pct(g, var, WEIGHT_VAR)
                rows.append(dict(wave=wave, variable=var, label=lab,
                                 subgroup_var=sname, subgroup_value=val,
                                 weighted_pct=pct, unweighted_base=base,
                                 small_base=base < SMALL_BASE))
    return pd.DataFrame(rows)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("microdata", help="Path to .sav or .csv microdata")
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--out", default="estimates.csv")
    args = ap.parse_args(argv)

    df, labels = read_microdata(args.microdata)
    print(f"Loaded {len(df):,} respondents, {len(df.columns):,} columns")
    scope = find_in_scope_vars(labels)
    print(f"In-scope variables matched: {len(scope)}")
    for v, l in scope.items():
        print(f"  {v}: {l}")
    est = build_estimates(df, labels, args.wave)
    est.to_csv(args.out, index=False)
    print(f"\nWrote {len(est):,} estimate rows -> {args.out}")
    # Show the overall in-scope headline figures
    head = est[est.subgroup_var == "ALL"][["label", "weighted_pct", "unweighted_base"]]
    print("\nOverall weighted figures (in scope):")
    print(head.to_string(index=False))


if __name__ == "__main__":
    main()
