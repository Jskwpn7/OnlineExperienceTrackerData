"""Shared pipeline sanity checks — fail loudly rather than silently drop or duplicate data."""
import pandas as pd

KEY = ["wave", "basis", "question", "metric", "item", "subgroup", "subgroup_value"]


def short(label, limit=80):
    """Shorten a response label for display. The old 48-char hard truncation
    merged distinct options (Q34 codes 2/6, Q45 codes 1/2) into identical
    labels, producing conflicting duplicate rows. 80 chars keeps all current
    labels distinct; assert_unique() is the backstop if a future label collides."""
    s = str(label)
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"


def assert_waves_mapped(df, source=""):
    """After deriving wave from starttime via MONTH2WAVE, ensure no records were
    left unmapped (a new wave's fieldwork months would otherwise be silently
    dropped by groupby)."""
    if df["wave"].isna().any():
        st = pd.to_datetime(df["starttime"], errors="coerce")
        months = sorted(set(st.dt.to_period("M").astype(str)[df["wave"].isna()]))
        raise SystemExit(
            f"[{source}] {int(df['wave'].isna().sum())} records have fieldwork months "
            f"not in MONTH2WAVE: {months} — add the new wave's months to the map."
        )


def assert_unique(df, source=""):
    """Every (wave, basis, question, metric, item, subgroup, subgroup_value)
    must be unique — duplicates mean a label collision or a double-append."""
    dup = df.duplicated(KEY)
    if dup.any():
        ex = df[df.duplicated(KEY, keep=False)].sort_values(KEY)
        raise SystemExit(
            f"[{source}] {int(dup.sum())} duplicate estimate keys (label collision?):\n"
            + ex[KEY + ["weighted_pct"]].head(8).to_string()
        )
