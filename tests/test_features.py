import pandas as pd

from churn.features import build_features


def test_build_features_one_hot_and_ratio():
    df = pd.DataFrame({"plan": ["basic", "premium"],
                       "monthly_spend": [100.0, 900.0],
                       "tenure_months": [12, 0],
                       "support_tickets": [2, 1]})
    X = build_features(df)
    assert list(X.columns) == ["monthly_spend", "tenure_months",
                               "support_tickets", "tickets_per_year", "tenure_bucket",
                               "plan_basic", "plan_premium"]
    assert X.loc[0, "tickets_per_year"] == 1.0
    assert X["plan_premium"].tolist() == [0, 1]


def test_tenure_bucket_boundaries():
    df = pd.DataFrame({"plan": ["basic"] * 4, "monthly_spend": [1.0] * 4,
                       "tenure_months": [0, 6, 7, 25], "support_tickets": [0] * 4})
    assert build_features(df)["tenure_bucket"].tolist() == [0, 0, 1, 3]
