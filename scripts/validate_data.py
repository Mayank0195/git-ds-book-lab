"""Validate customer CSV files against the data contract.

Usage: python scripts/validate_data.py CSV [CSV ...]
"""

import sys

import pandas as pd
import pandera.pandas as pa

SCHEMA = pa.DataFrameSchema(
    {
        "customer_id": pa.Column(str, unique=True),
        "plan": pa.Column(str, pa.Check.isin(["basic", "standard", "premium"])),
        "monthly_spend": pa.Column(float, pa.Check.ge(0)),
        "tenure_months": pa.Column(int, pa.Check.in_range(0, 600)),
        "support_tickets": pa.Column(int, pa.Check.ge(0)),
        "churned": pa.Column(int, pa.Check.isin([0, 1])),
    },
    coerce=True,
)


def main(paths: list[str]) -> int:
    failed = 0
    for path in paths:
        try:
            SCHEMA.validate(pd.read_csv(path), lazy=True)
            print(f"{path}: OK")
        except pa.errors.SchemaErrors as err:
            failed += 1
            cases = err.failure_cases[["column", "check", "failure_case"]]
            print(f"{path}: {len(cases)} problem(s)\n{cases.to_string(index=False)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
