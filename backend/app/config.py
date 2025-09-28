from pathlib import Path
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET_TO_A_STRONG_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

BASE_DIR = Path(__file__).parent

# CSVs ficam dentro de backend/data
DATA_DIR = BASE_DIR.parent / "data"
USERS_CSV = DATA_DIR / "users.csv"
METRICS_CSV = DATA_DIR / "metrics.csv"

# Frontend fora do backend
FRONTEND_DIR = BASE_DIR.parent.parent / "frontend"
