import pandas as pd
from .config import USERS_CSV, METRICS_CSV
from .utils import find_column

def load_csv(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"⚠️ Arquivo não encontrado: {path}")
        return pd.DataFrame()

users_df = load_csv(USERS_CSV)
metrics_df = load_csv(METRICS_CSV)

# Descobrir colunas dinamicamente
login_col = find_column(users_df, ["email", "e-mail", "mail", "username"])
password_col = find_column(users_df, ["password", "pass", "senha"])
role_col = find_column(users_df, ["role", "papel", "perfil"])
date_col = find_column(metrics_df, ["date", "dia", "ds"])

if date_col:
    try:
        metrics_df[date_col] = pd.to_datetime(metrics_df[date_col], errors="coerce")
    except Exception:
        pass
