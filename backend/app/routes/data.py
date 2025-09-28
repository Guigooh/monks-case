import pandas as pd
from fastapi import APIRouter, Depends
from ..auth import get_current_user
from ..database import metrics_df, date_col

router = APIRouter(prefix="/api", tags=["data"])

@router.get("/columns")
async def columns(user=Depends(get_current_user)):
    cols = list(metrics_df.columns)
    if "cost_micros" in cols and (user.get("role") or "").lower() != "admin":
        cols.remove("cost_micros")
    return {"columns": cols}

@router.get("/data")
async def get_data(
    start_date: str | None = None,
    end_date: str | None = None,
    order_by: str | None = None,
    order_dir: str = "asc",
    page: int = 1,
    page_size: int = 50,
    user=Depends(get_current_user),
):
    df = metrics_df.copy()
    if date_col:
        if start_date:
            s = pd.to_datetime(start_date, errors="coerce")
            if pd.notna(s):
                df = df[df[date_col] >= s]
        if end_date:
            e = pd.to_datetime(end_date, errors="coerce")
            if pd.notna(e):
                df = df[df[date_col] <= e]
    if order_by and order_by in df.columns:
        df = df.sort_values(by=order_by, ascending=(order_dir == "asc"))
    if (user.get("role") or "").lower() != "admin" and "cost_micros" in df.columns:
        df = df.drop(columns=["cost_micros"])
    total = len(df)
    start = (page - 1) * page_size
    end = start + page_size
    page_df = df.iloc[start:end].copy()
    for c in page_df.select_dtypes(include=["datetime64"]).columns:
        page_df[c] = page_df[c].dt.strftime("%Y-%m-%d")
    records = page_df.fillna("").to_dict(orient="records")
    return {"data": records, "total": total, "page": page, "page_size": page_size}
