"""Feature engineering for the churn model."""

import pandas as pd

NUMERIC = ["monthly_spend", "tenure_months", "support_tickets"]

# Tenure buckets in months: 0-6, 7-12, 13-24, 25+ (upper edges inclusive).
TENURE_BINS = [0, 6, 12, 24, 600]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Numeric features, a tenure bucket and one-hot encoded plan."""
    X = df[NUMERIC].copy()
    X["tickets_per_year"] = df["support_tickets"] / (df["tenure_months"] / 12 + 1)
    X["tenure_bucket"] = pd.cut(
        df["tenure_months"], bins=TENURE_BINS, labels=False, include_lowest=True
    )
    plans = pd.get_dummies(df["plan"], prefix="plan", dtype=int)
    return pd.concat([X, plans], axis=1)
