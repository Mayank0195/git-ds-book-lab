import joblib
import pytest
from fastapi.testclient import TestClient
from sklearn.linear_model import LogisticRegression

from churn import api
from churn.data import load_customers
from churn.features import build_features


@pytest.fixture
def client(tmp_path, monkeypatch):
    df = load_customers("tests/fixtures/customers_sample.csv")
    model = LogisticRegression(max_iter=1000).fit(build_features(df), df["churned"])
    joblib.dump(model, tmp_path / "model.joblib")
    monkeypatch.setenv("CHURN_MODEL", str(tmp_path / "model.joblib"))
    monkeypatch.setattr(api, "_model", None)
    return TestClient(api.app)


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_predict_returns_a_probability(client):
    body = {"plan": "basic", "monthly_spend": 50, "tenure_months": 3, "support_tickets": 4}
    r = client.post("/predict", json=body)
    assert r.status_code == 200
    assert 0.0 <= r.json()["churn_probability"] <= 1.0


def test_predict_rejects_negative_spend(client):
    body = {"plan": "basic", "monthly_spend": -1, "tenure_months": 3, "support_tickets": 4}
    assert client.post("/predict", json=body).status_code == 422
