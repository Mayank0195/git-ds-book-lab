#!/usr/bin/env bash
# A tour of DVC data versioning, run on a GitHub runner (Chapter 19).
set -euo pipefail
step() { printf '\n=== %s\n' "$*"; }
git config user.name "Asha Rao"; git config user.email "asha.rao@example.com"

step "dvc init and a local remote"
dvc init -q
dvc remote add -d storage /tmp/dvc-storage
cat .dvc/config

step "dvc add: track the dataset"
mkdir -p data && cp tests/fixtures/customers_sample.csv data/customers.csv
dvc add data/customers.csv
cat data/customers.csv.dvc
cat data/.gitignore
git add .dvc data/customers.csv.dvc data/.gitignore
git commit -q -m "data: track customers.csv with DVC (200 rows)"

step "dvc push: cache to remote"
dvc push
find /tmp/dvc-storage -type f | sed 's|/tmp/dvc-storage/||'

step "lose the data, dvc pull it back"
rm -rf .dvc/cache data/customers.csv
dvc pull -q
wc -l < data/customers.csv

step "a new data version"
head -n 101 data/customers.csv > /tmp/v2.csv && cp /tmp/v2.csv data/customers.csv
dvc status
dvc add -q data/customers.csv
git commit -q -am "data: customers.csv v2 (100 rows)"
dvc push -q
dvc diff HEAD~1

step "back to the first data version"
git checkout -q HEAD~1 -- data/customers.csv.dvc
dvc checkout
wc -l < data/customers.csv
git log --oneline -- data/customers.csv.dvc
