import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from fastapi.staticfiles import StaticFiles

SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET_TO_A_STRONG_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
USERS_CSV = DATA_DIR / "users.csv"
METRICS_CSV = DATA_DIR / "metrics.csv"

app = FastAPI(
    title="Monks Case API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

def load_csv(path: Path):
    if not path.exists():
        print(f"⚠️  Arquivo não encontrado: {path}")
        return pd.DataFrame()
    return pd.read_csv(path)

users_df = load_csv(USERS_CSV)
metrics_df = load_csv(METRICS_CSV)

def find_column(df, candidates):
    if df is None or df.empty:
        return None
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        for k in cols:
            if cand in k:
                return cols[k]
    return None

login_col = find_column(users_df, ["email", "e-mail", "mail", "username"])
password_col = find_column(users_df, ["password", "pass", "senha"])
role_col = find_column(users_df, ["role", "papel", "perfil"])

date_col = find_column(metrics_df, ["date", "dia", "ds"])
if date_col:
    try:
        metrics_df[date_col] = pd.to_datetime(metrics_df[date_col], errors="coerce")
    except Exception:
        pass

security = HTTPBearer()

class LoginIn(BaseModel):
    email: str
    password: str

def authenticate_user(email: str, password: str):
    if users_df.empty or login_col is None:
        return None
    mask = users_df[login_col].astype(str).str.lower() == email.lower()
    matched = users_df[mask]
    if matched.empty:
        return None
    row = matched.iloc[0]
    stored_password = str(row[password_col]) if password_col else ""
    if stored_password != password:
        return None
    role = row[role_col] if role_col else "user"
    return {"email": row[login_col], "role": str(role)}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

@app.post("/api/login")
async def login(payload: LoginIn):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/me")
async def me(user=Depends(get_current_user)):
    return user

@app.get("/api/columns")
async def columns(user=Depends(get_current_user)):
    cols = list(metrics_df.columns)
    if "cost_micros" in cols and (user.get("role") or "").lower() != "admin":
        cols.remove("cost_micros")
    return {"columns": cols}

@app.get("/api/data")
async def get_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    order_by: Optional[str] = None,
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

FRONTEND_DIR = BASE_DIR.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
