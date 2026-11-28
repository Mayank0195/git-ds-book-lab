"""HTTP API for the churn model: GET /health and POST /predict."""

import os
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from churn import __version__
from churn.features import build_features

app = FastAPI(title="churn", version=__version__)
_model: Any = None


class Customer(BaseModel):
    plan: str
    monthly_spend: float = Field(ge=0)
    tenure_months: int = Field(ge=0)
    support_tickets: int = Field(ge=0)


def get_model() -> Any:
    global _model
    if _model is None:
        _model = joblib.load(os.environ.get("CHURN_MODEL", "models/model.joblib"))
    return _model


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/predict")
def predict(customer: Customer) -> dict[str, float]:
    model = get_model()
    X = build_features(pd.DataFrame([customer.model_dump()]))
    X = X.reindex(columns=model.feature_names_in_, fill_value=0)
    return {"churn_probability": round(float(model.predict_proba(X)[0, 1]), 4)}
