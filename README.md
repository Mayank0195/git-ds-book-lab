# churn-model

Predict which customers of a subscription service will cancel next month,
so that the retention team can contact them first.

## Data

`customers.csv`: 1,200 synthetic customers with plan, monthly spend, tenure,
support tickets and the label `churned` (1 = cancelled). The data is generated
for teaching and contains no real people. It is not stored in this repository;
place it in `data/raw/`.

## Quick start

~~~bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
PYTHONPATH=src python -m churn.train data/raw/customers.csv
~~~

## Project layout

| Path | Contents |
|---|---|
| `src/churn/` | Python package: data loading, features, training |
| `tests/` | Unit tests (pytest) |
| `notebooks/` | Exploration only; reusable code moves to `src/` |
| `data/`, `models/` | Local data and artefacts, not tracked by Git |

## Results

Logistic regression on six features: test AUC is printed by the training
script (see the commit history for changes).

## License

MIT, see `LICENSE`.
- Remotes: see Chapter 10 of the book.
