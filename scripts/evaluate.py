"""Train, evaluate on a held-out split, log to MLflow and write reports/metrics.json.

Usage: PYTHONPATH=src python scripts/evaluate.py DATA_CSV [--out reports]
Parameters come from params.yaml (section "train").
"""

import argparse
import json
import os
from pathlib import Path

import mlflow
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from churn.data import load_customers
from churn.features import build_features


def make_model(p: dict):
    if p["model"] == "logreg":
        clf = LogisticRegression(C=p["C"], max_iter=1000, class_weight="balanced")
        return make_pipeline(StandardScaler(), clf)
    if p["model"] == "tree":
        return DecisionTreeClassifier(max_depth=p["max_depth"], random_state=p["seed"])
    raise ValueError(f"unknown model {p['model']!r}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--out", default="reports")
    args = ap.parse_args()
    p = yaml.safe_load(Path("params.yaml").read_text())["train"]

    df = load_customers(args.data)
    X, y = build_features(df), df["churned"]
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=p["test_size"], stratify=y, random_state=p["seed"]
    )
    commit = os.environ.get("GITHUB_SHA", "local")[:7]
    mlflow.set_experiment("churn-ci")
    with mlflow.start_run(run_name=f"{p['model']}-{commit}") as run:
        model = make_model(p).fit(X_tr, y_tr)
        proba = model.predict_proba(X_te)[:, 1]
        metrics = {
            "auc": round(float(roc_auc_score(y_te, proba)), 4),
            "accuracy": round(float(accuracy_score(y_te, proba >= 0.5)), 4),
            "n_train": len(X_tr),
            "n_test": len(X_te),
        }
        mlflow.log_params(p)
        mlflow.log_metrics({"auc": metrics["auc"], "accuracy": metrics["accuracy"]})
        mlflow.set_tag("git_commit", commit)

    out = Path(args.out)
    out.mkdir(exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics), f"mlflow_run={run.info.run_id[:8]}")


if __name__ == "__main__":
    main()
