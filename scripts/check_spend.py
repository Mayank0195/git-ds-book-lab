"""Count rows with negative monthly_spend (issue: negative spend in extracts)."""
import sys

import pandas as pd

df = pd.read_csv(sys.argv[1])
print(f"{(df['monthly_spend'] < 0).sum()} of {len(df)} rows have negative monthly_spend")
