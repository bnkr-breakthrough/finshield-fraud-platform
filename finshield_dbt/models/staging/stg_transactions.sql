{{ config(materialized='view') }}

select
    transaction_id,
    customer_id,
    customer_name,
    city,
    amount,
    merchant,
    payment_type,
    transaction_status,
    fraud_decision,
    fraud_flag,
    fraud_severity,
    fraud_score,
    fraud_reason,
    risk_level,
    account_status,
    event_timestamp
from {{ source('raw', 'transactions') }}
