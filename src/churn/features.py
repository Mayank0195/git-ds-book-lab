"""Feature engineering for the churn model."""
import os

import pandas as pd

NUMERIC = ["monthly_spend", "tenure_months", "support_tickets"]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Numeric features plus one-hot encoded plan."""
    X = df[NUMERIC].copy()
    X["tickets_per_year"] = df["support_tickets"] / (df["tenure_months"] / 12 + 1)
    plans = pd.get_dummies(df["plan"], prefix="plan", dtype=int)
    return pd.concat([X, plans], axis=1)
