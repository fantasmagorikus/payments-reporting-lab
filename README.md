# Payments Reporting Lab

Small, reproducible lab that processes card acceptance and chargeback extracts with Python and matches the same answers in SQL.

## What it covers
- Monthly acceptance rate from raw events.
- Declined volume by country with a threshold filter.
- Reconciliation of acceptance refs against chargebacks.
- One-to-one parity between Python steps and `analysis/sql_answers.sql`.

## Layout
- `acceptance.csv`, `chargeback.csv`: source data.
- `analysis/`: Python scripts, CSV outputs, and `sql_answers.sql`.
- `init/create_tables.sql`: minimal DDL for Postgres validation.
- `docker-compose.yml`: starts Postgres 16 with the DDL mounted.

## Data source (mock)
- Data is mock transaction-like CSVs for a fictional payments provider. No production or live data.
- Public payment data references for context:
  - https://datahub.io/MachineShop/ecommerce-payments (example ecommerce payment dataset)
  - https://www.kaggle.com/code/joebeachcapital/credit-card-transaction-data (example card transaction demo)
- APIs: this lab works entirely offline on static CSVs; no payment gateways or external APIs are called. In a real flow, these same transforms could sit in front of ingestion APIs or warehouse tables exposed by a PSP.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analysis/q1_acceptance_rate.py
python analysis/q2_declined_countries.py
python analysis/q3_missing_chargebacks.py
```
Each script prints its result and writes a CSV next to the code.

## Analysis steps
- Q1 `q1_acceptance_rate.py`: bucket `date_time` by month, count total vs accepted, compute acceptance rate. SQL match: `DATE_TRUNC` + filtered `COUNT(*)` in `analysis/sql_answers.sql`.
- Q2 `q2_declined_countries.py`: coerce `amount`, keep `DECLINED`, sum by `country`, keep totals above 25,000,000. SQL match: `SUM(amount)` + `HAVING SUM(amount) > 25000000`.
- Q3 `q3_missing_chargebacks.py`: normalize `external_ref` to strings, left join chargebacks to acceptance, return acceptance refs missing in chargebacks. SQL match: left join + `WHERE c.external_ref IS NULL`.

## SQL validation (optional)
```bash
docker-compose up -d
```
Load `acceptance.csv` and `chargeback.csv` into the tables from `init/create_tables.sql`, then run `analysis/sql_answers.sql`. Results should align with the Python outputs.

## Notes
- No secrets are stored here. Compose uses demo-only creds (`labuser` / `labpass`) for local checks.
- Replace or redact the bundled data if needed before sharing further.
