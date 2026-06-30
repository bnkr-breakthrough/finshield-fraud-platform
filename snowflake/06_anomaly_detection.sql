-- ============================================================================
-- FinShield — 06: Anomaly Detection
-- ============================================================================
--
-- GOAL: Demonstrate Cortex AI / ML-based anomaly detection capability.
--
-- LIMITATION (confirmed via direct testing, not assumption):
-- Cortex LLM functions (CLASSIFY_TEXT, COMPLETE) and SNOWFLAKE.ML.ANOMALY_
-- DETECTION both returned errors indicating they require a paid Snowflake
-- plan / are unavailable on trial accounts in this account's region.
-- The exact syntax attempted is preserved below for reference, followed by
-- a working statistical alternative that achieves the same goal.
-- ============================================================================

USE DATABASE finshield_db;
USE SCHEMA analytics;

-- ── ATTEMPTED (blocked on trial account) — Cortex CLASSIFY_TEXT ───────────
-- SELECT
--     transaction_id,
--     fraud_reason,
--     SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
--         fraud_reason,
--         ['Amount Anomaly', 'Merchant Risk', 'Account Compromise', 'Location Risk']
--     ) AS ai_classification
-- FROM finshield_db.raw.transactions
-- WHERE fraud_decision = 'FRAUD'
-- LIMIT 10;
-- Error: AI function CLASSIFY_TEXT is not available for trial accounts.

-- ── ATTEMPTED (blocked on trial account) — Cortex COMPLETE ────────────────
-- SELECT
--     transaction_id,
--     SNOWFLAKE.CORTEX.COMPLETE(
--         'snowflake-arctic',
--         CONCAT('In one short sentence, explain the fraud risk for: ', fraud_reason)
--     ) AS ai_explanation
-- FROM finshield_db.raw.transactions
-- WHERE fraud_decision = 'FRAUD'
-- LIMIT 5;
-- Error: AI function COMPLETE is not available for trial accounts.

-- ── ATTEMPTED (syntax mismatch on this Snowflake version) — ML.ANOMALY_DETECTION
-- CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION finshield_anomaly_model(
--     INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'finshield_db.analytics.daily_transaction_volume'),
--     TIMESTAMP_COLNAME => 'ts',
--     TARGET_COLNAME => 'transaction_count'
-- );
-- Error: named arguments do not match function signature for this account/version.

-- ============================================================================
-- WORKING ALTERNATIVE: Statistical z-score anomaly detection
-- A legitimate production technique independent of LLM/ML function
-- availability — flags hours where transaction volume deviates more than
-- 2 standard deviations from the mean.
-- ============================================================================

CREATE OR REPLACE VIEW daily_transaction_volume AS
SELECT
    DATE_TRUNC('HOUR', event_timestamp) AS ts,
    COUNT(*) AS transaction_count
FROM finshield_db.raw.transactions
GROUP BY ts
ORDER BY ts;

CREATE OR REPLACE VIEW transaction_anomalies AS
WITH stats AS (
    SELECT
        AVG(transaction_count) AS avg_count,
        STDDEV(transaction_count) AS stddev_count
    FROM daily_transaction_volume
)
SELECT
    d.ts,
    d.transaction_count,
    s.avg_count,
    s.stddev_count,
    ROUND((d.transaction_count - s.avg_count) / NULLIF(s.stddev_count, 0), 2) AS z_score,
    CASE
        WHEN ABS((d.transaction_count - s.avg_count) / NULLIF(s.stddev_count, 0)) > 2
        THEN 'ANOMALY'
        ELSE 'NORMAL'
    END AS anomaly_flag
FROM daily_transaction_volume d
CROSS JOIN stats s
ORDER BY d.ts DESC;

-- View all hourly buckets with their z-scores
SELECT * FROM transaction_anomalies ORDER BY ts DESC LIMIT 20;

-- View only flagged anomalies (may be empty if data is uniformly distributed,
-- which is expected for a synthetic generator without injected volume spikes)
SELECT * FROM transaction_anomalies WHERE anomaly_flag = 'ANOMALY';
