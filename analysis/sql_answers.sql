-- SQL answers matching the Python analysis scripts.
-- Tables defined in init/create_tables.sql:
--   globepay_acceptance_report (external_ref, date_time, state, cvv_provided, amount, country, currency, rates)
--   globepay_chargeback_report (external_ref, status, source, chargeback)

-- Q1: Acceptance rate by month
SELECT
    DATE_TRUNC('month', date_time) AS month,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE UPPER(state) = 'ACCEPTED') AS accepted,
    ROUND(100.0 * COUNT(*) FILTER (WHERE UPPER(state) = 'ACCEPTED') / NULLIF(COUNT(*), 0), 2) AS acceptance_rate
FROM globepay_acceptance_report
GROUP BY 1
ORDER BY 1;

-- Q2: Countries with declined amount > 25M
SELECT
    country,
    SUM(amount) AS declined_amount
FROM globepay_acceptance_report
WHERE UPPER(state) = 'DECLINED'
GROUP BY country
HAVING SUM(amount) > 25000000
ORDER BY declined_amount DESC;

-- Q3: Acceptance records missing in chargeback
SELECT a.external_ref
FROM globepay_acceptance_report a
LEFT JOIN globepay_chargeback_report c
  ON a.external_ref = c.external_ref
WHERE c.external_ref IS NULL
ORDER BY a.external_ref;
