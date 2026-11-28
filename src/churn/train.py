"""Train a churn classifier and print its test AUC.

Usage: python -m churn.train DATA_CSV
"""

import sys

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from churn.data import load_customers
from churn.features import build_features


def main(path: str) -> float:
    df = load_customers(path)
    X, y = build_features(df), df["churned"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    model = make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")
    )
    model.fit(X_tr, y_tr)
    auc = float(roc_auc_score(y_te, model.predict_proba(X_te)[:, 1]))
    print(f"test AUC = {auc:.4f}")
    return auc


if __name__ == "__main__":
    main(sys.argv[1])
