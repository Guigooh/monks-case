import pandas as pd
from app.database import load_csv

def test_load_csv_not_found(tmp_path):
    fake_file = tmp_path / "missing.csv"
    df = load_csv(fake_file)
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_load_csv_found(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("email,password\nuser@test.com,123")
    df = load_csv(csv_file)
    assert not df.empty
    assert list(df.columns) == ["email", "password"]
    assert df.iloc[0]["email"] == "user@test.com"
