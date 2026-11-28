"""Load and validate the raw customer table."""
from pathlib import Path

import pandas as pd

REQUIRED = ["customer_id", "plan", "monthly_spend", "tenure_months",
            "support_tickets", "churned"]


def load_customers(path: str | Path) -> pd.DataFrame:
    """Read the customer CSV and check that the required columns exist."""
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    return df
