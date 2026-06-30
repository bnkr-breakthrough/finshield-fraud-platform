-- ============================================================================
-- FinShield — 02: Snowpipe (File Ingestion)
-- ============================================================================

USE DATABASE finshield_db;
USE SCHEMA raw;

-- ── File format for CSV ingestion ───────────────────────────────────────────
CREATE OR REPLACE FILE FORMAT finshield_csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE;

-- ── Internal stage for incoming files ──────────────────────────────────────
CREATE OR REPLACE STAGE finshield_stage
    FILE_FORMAT = finshield_csv_format;

-- ── Pipe: auto-loads new files from the stage into the transactions table ──
-- Note: AUTO_INGEST is FALSE here because true auto-ingest requires an
-- S3/GCS event notification integration, which needs IAM permissions beyond
-- a trial account's scope. Ingestion mechanics (stage -> pipe -> COPY INTO)
-- are otherwise identical to production Snowpipe; only the trigger differs.
CREATE OR REPLACE PIPE finshield_db.raw.transactions_pipe
    AUTO_INGEST = FALSE
    AS
    COPY INTO finshield_db.raw.transactions (
        transaction_id, customer_id, customer_name, city, amount, merchant,
        payment_type, transaction_status, fraud_decision, fraud_flag,
        fraud_severity, fraud_score, fraud_reason, risk_level,
        account_status, event_timestamp
    )
    FROM @finshield_db.raw.finshield_stage
    FILE_FORMAT = (FORMAT_NAME = 'finshield_db.raw.finshield_csv_format')
    ON_ERROR = 'CONTINUE';

-- Verify pipe was created
SHOW PIPES IN SCHEMA finshield_db.raw;

-- ── Usage: upload a CSV file to the stage (via Snowsight UI or PUT command),
--    then trigger ingestion manually with: ──────────────────────────────────
-- ALTER PIPE finshield_db.raw.transactions_pipe REFRESH;

-- Check pipe status
-- SELECT SYSTEM$PIPE_STATUS('finshield_db.raw.transactions_pipe');

-- Check what's currently staged
-- LIST @finshield_db.raw.finshield_stage;

-- Verify ingestion via copy history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'FINSHIELD_DB.RAW.TRANSACTIONS',
    START_TIME => DATEADD(HOURS, -24, CURRENT_TIMESTAMP())
))
ORDER BY LAST_LOAD_TIME DESC;
