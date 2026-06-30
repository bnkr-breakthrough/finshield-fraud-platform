-- ============================================================================
-- FinShield — 03: Streams & Tasks (CDC + Automated Processing)
-- ============================================================================

USE DATABASE finshield_db;
USE SCHEMA raw;

-- ── Stream: captures row-level changes (CDC) on the transactions table ─────
CREATE OR REPLACE STREAM transactions_stream
    ON TABLE finshield_db.raw.transactions
    APPEND_ONLY = TRUE;

SHOW STREAMS IN SCHEMA finshield_db.raw;

-- Check stream has data (returns 0 if no new rows since stream creation)
SELECT COUNT(*) FROM transactions_stream;

-- ── Summary log table that the task will write into ─────────────────────────
USE SCHEMA analytics;

CREATE TABLE IF NOT EXISTS fraud_summary_log (
    log_id              INTEGER AUTOINCREMENT,
    processed_at        TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    new_transactions    INTEGER,
    new_fraud_count     INTEGER,
    new_fraud_amount    FLOAT
);

-- ── Task: runs every 1 minute, but only executes when the stream has data ──
-- This conditional WHEN clause avoids wasted compute on empty checks —
-- the task is SKIPPED (not run) when there's nothing new to process.
USE SCHEMA raw;

CREATE OR REPLACE TASK process_fraud_stream
    WAREHOUSE = finshield_wh
    SCHEDULE = '1 MINUTE'
WHEN
    SYSTEM$STREAM_HAS_DATA('transactions_stream')
AS
INSERT INTO finshield_db.analytics.fraud_summary_log (new_transactions, new_fraud_count, new_fraud_amount)
SELECT
    COUNT(*) AS new_transactions,
    SUM(CASE WHEN fraud_decision = 'FRAUD' THEN 1 ELSE 0 END) AS new_fraud_count,
    SUM(CASE WHEN fraud_decision = 'FRAUD' THEN amount ELSE 0 END) AS new_fraud_amount
FROM transactions_stream;

-- Tasks are created SUSPENDED by default — must explicitly resume
ALTER TASK process_fraud_stream RESUME;

-- Verify task is running
SHOW TASKS IN SCHEMA finshield_db.raw;

-- ── To test: insert a row, wait ~60-90s, then check the log table ─────────
-- INSERT INTO finshield_db.raw.transactions (...) VALUES (...);
-- SELECT * FROM finshield_db.analytics.fraud_summary_log ORDER BY processed_at DESC;

-- Check task execution history (shows SKIPPED vs SUCCEEDED runs)
SELECT *
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    TASK_NAME => 'PROCESS_FRAUD_STREAM',
    SCHEDULED_TIME_RANGE_START => DATEADD('HOUR', -1, CURRENT_TIMESTAMP())
))
ORDER BY SCHEDULED_TIME DESC;

-- ── IMPORTANT: suspend the task when not actively demoing ──────────────────
-- A 1-minute schedule runs forever and consumes compute credits even when
-- idle (though SKIPPED runs are cheap). Suspend between demo sessions:
-- ALTER TASK process_fraud_stream SUSPEND;
