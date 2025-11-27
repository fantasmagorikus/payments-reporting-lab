CREATE TABLE IF NOT EXISTS globepay_acceptance_report (
    external_ref TEXT,
    date_time TIMESTAMP,
    state TEXT,
    cvv_provided TEXT,
    amount NUMERIC,
    country TEXT,
    currency TEXT,
    rates TEXT
);

CREATE TABLE IF NOT EXISTS globepay_chargeback_report (
    external_ref TEXT,
    status TEXT,
    source TEXT,
    chargeback TEXT
);
