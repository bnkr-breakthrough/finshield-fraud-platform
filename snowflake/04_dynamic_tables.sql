-- ============================================================================
-- FinShield — 04: Dynamic Tables (Self-Maintaining Aggregates)
-- ============================================================================

USE DATABASE finshield_db;
USE SCHEMA analytics;

-- Dynamic Tables auto-refresh based on their defining query — Snowflake
-- handles incremental refresh automatically. No manual stream/task wiring
-- needed, unlike the Streams & Tasks pattern in 03_streams_tasks.sql.

CREATE OR REPLACE DYNAMIC TABLE fraud_severity_summary
    TARGET_LAG = '1 minute'
    WAREHOUSE = finshield_wh
AS
SELECT
    fraud_severity,
    city,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(fraud_score) AS avg_fraud_score
FROM finshield_db.raw.transactions
WHERE fraud_decision = 'FRAUD'
GROUP BY fraud_severity, city;

-- Verify data
SELECT * FROM fraud_severity_summary
ORDER BY transaction_count DESC;

-- Check configuration (target_lag, refresh_mode, scheduling_state)
SHOW DYNAMIC TABLES IN SCHEMA finshield_db.analytics;

-- Check refresh history — proves Snowflake is automatically refreshing
-- this table on schedule without any manual intervention
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => 'finshield_db.analytics.fraud_severity_summary'
))
ORDER BY refresh_start_time DESC;
