-- ============================================================================
-- FinShield — 05: Snowpark Python UDF (Risk Scoring)
-- ============================================================================

USE DATABASE finshield_db;
USE SCHEMA analytics;

-- A Python UDF running natively inside Snowflake's compute engine.
-- Combines fraud score, transaction amount, and account status into a
-- single risk score capped at 100.
CREATE OR REPLACE FUNCTION calculate_risk_score(
    amount FLOAT,
    fraud_score INTEGER,
    account_status STRING
)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.10'
HANDLER = 'risk_calc'
AS
$$
def risk_calc(amount, fraud_score, account_status):
    base_risk = fraud_score * 0.6
    amount_factor = min(amount / 1000, 40)
    status_penalty = 20 if account_status == 'Blocked' else (10 if account_status == 'Suspended' else 0)
    total = base_risk + amount_factor + status_penalty
    return round(min(total, 100), 2)
$$;

-- Test the UDF against real fraud transactions
SELECT
    transaction_id,
    customer_name,
    amount,
    fraud_score,
    account_status,
    calculate_risk_score(amount, fraud_score, account_status) AS computed_risk_score
FROM finshield_db.raw.transactions
WHERE fraud_decision = 'FRAUD'
ORDER BY computed_risk_score DESC
LIMIT 15;

-- ── Known observation: many fraud transactions saturate at the 100 cap ─────
-- because amount, fraud_score, and account_status compound additively in
-- this dataset's fraud profile. A future iteration would weight amount
-- logarithmically rather than linearly for better score distribution.
