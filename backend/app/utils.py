def find_column(df, candidates):
    if df is None or df.empty:
        return None
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        for k in cols:
            if cand in k:
                return cols[k]
    return None
