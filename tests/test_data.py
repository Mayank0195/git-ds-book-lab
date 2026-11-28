import pandas as pd
import pytest

from churn.data import load_customers


def test_load_customers_reads_sample():
    df = load_customers("tests/fixtures/customers_sample.csv")
    assert len(df) == 200


def test_load_customers_rejects_missing_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"customer_id": ["C1"], "plan": ["basic"]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="missing columns"):
        load_customers(path)
