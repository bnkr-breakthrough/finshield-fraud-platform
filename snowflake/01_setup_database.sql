-- ============================================================================
-- FinShield — 01: Database, Schema, Warehouse & Table Setup
-- ============================================================================

CREATE WAREHOUSE IF NOT EXISTS finshield_wh
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

CREATE DATABASE IF NOT EXISTS finshield_db;

CREATE SCHEMA IF NOT EXISTS finshield_db.raw;
CREATE SCHEMA IF NOT EXISTS finshield_db.analytics;

USE WAREHOUSE finshield_wh;
USE DATABASE finshield_db;
USE SCHEMA raw;

-- ── Transactions table ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id      STRING,
    customer_id         STRING,
    customer_name       STRING,
    city                 STRING,
    amount               FLOAT,
    merchant             STRING,
    payment_type         STRING,
    transaction_status   STRING,
    fraud_decision       STRING,
    fraud_flag           STRING,
    fraud_severity       STRING,
    fraud_score          INTEGER,
    fraud_reason         STRING,
    risk_level           STRING,
    account_status       STRING,
    event_timestamp      TIMESTAMP_NTZ,
    loaded_at            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Verify
SELECT COUNT(*) AS total_rows FROM transactions;
