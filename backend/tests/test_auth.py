import pytest
from datetime import timedelta
from jose import jwt
from app.auth import create_access_token, authenticate_user
from app.config import SECRET_KEY, ALGORITHM
import pandas as pd
from app import database

def test_create_access_token():
    data = {"sub": "user@example.com", "role": "admin"}
    token = create_access_token(data, expires_delta=timedelta(minutes=5))
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "user@example.com"
    assert decoded["role"] == "admin"

def test_authenticate_user_not_found(monkeypatch):
    df = pd.DataFrame({"email": ["other@example.com"], "password": ["123"]})
    monkeypatch.setattr(database, "users_df", df)
    monkeypatch.setattr(database, "login_col", "email")
    monkeypatch.setattr(database, "password_col", "password")
    monkeypatch.setattr(database, "role_col", "role")

    user = authenticate_user("missing@example.com", "123")
    assert user is None
