{{ config(materialized='table') }}

select
    fraud_severity,
    city,
    count(*) as transaction_count,
    sum(amount) as total_amount,
    avg(fraud_score) as avg_fraud_score,
    sum(case when fraud_decision = 'FRAUD' then 1 else 0 end) as fraud_count
from {{ ref('stg_transactions') }}
group by fraud_severity, city
order by transaction_count desc
