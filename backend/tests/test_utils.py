import pandas as pd
from app.utils import find_column

def test_find_column_exact_match():
    df = pd.DataFrame({"email": ["a@a.com"], "senha": ["123"]})
    assert find_column(df, ["email"]) == "email"

def test_find_column_partial_match():
    df = pd.DataFrame({"user_email": ["a@a.com"]})
    assert find_column(df, ["email"]) == "user_email"

def test_find_column_not_found():
    df = pd.DataFrame({"name": ["joao"]})
    assert find_column(df, ["email"]) is None

def test_find_column_empty_df():
    df = pd.DataFrame()
    assert find_column(df, ["email"]) is None
