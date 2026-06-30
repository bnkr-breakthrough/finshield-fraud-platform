# FinShield — Interview Guide

This document is your preparation tool, not something to read verbatim. Internalize the structure, use your own words.

---

## The 90-Second Pitch

Use this when asked "tell me about a project you're proud of" or "walk me through your portfolio."

> "FinShield is a real-time fraud detection platform I built to apply my SnowPro Core, AWS, and Databricks certifications hands-on rather than just on paper.
>
> The architecture follows a standard streaming pattern: transactions flow through Kafka, get processed by PySpark Structured Streaming applying a multi-rule fraud engine — amount thresholds, merchant risk, account status, and location patterns — and land in Snowflake.
>
> On the Snowflake side, I implemented the full feature set: Snowpipe for ingestion, Streams and Tasks for change data capture and automated processing, Dynamic Tables for self-maintaining aggregates, and a Snowpark Python UDF for risk scoring. I also built a small dbt project with staging and mart models.
>
> The dashboard is a SOC-style real-time monitoring UI built in Streamlit, deployed live on Streamlit Community Cloud, so it's actually accessible right now, not just a local demo.
>
> One thing I'm particularly proud of: when I tried to use Cortex AI's LLM functions for anomaly detection, I discovered they're gated behind a paid plan on trial accounts. Rather than fake it, I implemented a statistical z-score based anomaly detector instead — which is actually a legitimate production technique on its own."

---

## Anticipated Questions & Strong Answers

### "Why didn't you use real production infrastructure for the live demo?"

> "Running Kafka brokers and a Spark cluster 24/7 isn't sustainable on a free budget, and I didn't want the portfolio link to go dark when a trial ends. So I split the project into two layers: the actual Kafka/Spark/Snowflake pipeline code is complete, tested, and in the GitHub repo — fully readable and explainable. The live dashboard runs on a lightweight Python simulator that mimics the same fraud-detection logic, so it stays online indefinitely on Streamlit's free tier. I think being upfront about that tradeoff is more credible than pretending a free demo is running production infrastructure."

### "Walk me through your Snowpipe setup."

> "I created a named internal stage with a CSV file format, then a pipe configured to COPY INTO the transactions table. Since true auto-ingest requires cloud storage event notifications — S3 or GCS integration with IAM roles — which is outside a trial account's scope, I triggered ingestion manually via `ALTER PIPE REFRESH`. The actual ingestion mechanics — stage, pipe, COPY INTO with file format and column mapping — are identical to what runs in production; only the trigger mechanism differs."

### "What was the hardest bug you ran into?"

> "When I first tested Snowpipe with a new batch file, it loaded zero rows. I checked copy history and found a column count mismatch — my source table had 16 columns but my Snowflake table had 17, because I'd added a `loaded_at` audit column with a default value. The fix was explicitly listing the 16 source columns in my COPY INTO statement so Snowflake only mapped those, letting `loaded_at` use its default. It taught me to always verify column counts match exactly when the schemas aren't identical, rather than assuming `COPY INTO` handles drift automatically."

### "Tell me about a feature that didn't work as expected."

> "I tried implementing Cortex AI's `CLASSIFY_TEXT` and `COMPLETE` functions for fraud reason classification and anomaly explanation. Both returned errors saying they're not available on trial accounts. Rather than skip the anomaly detection goal entirely, I implemented z-score based detection — flagging hours where transaction volume deviates more than two standard deviations from the mean. It's a real technique, and I documented the Cortex limitation honestly rather than claiming I'd used it."

### "How does your fraud detection logic actually work?"

> "It's rule-based, not ML-based, which was a deliberate choice for a portfolio project — it's explainable and auditable, which matters in fraud/compliance contexts. Four rules: transaction amount over a threshold, merchant risk category, blocked account status, and high-value transactions in flagged cities. A transaction is marked fraud if two or more rules trigger together, or with a smaller probability if only one rule fires — that mirrors how real systems combine weak signals rather than trusting any single indicator."

### "What would you change if you rebuilt this?"

> "Two things. First, I'd weight the risk score formula logarithmically rather than linearly — I noticed in testing that high-fraud transactions cluster at the score cap because amount, fraud score, and account status all compound additively. Second, I'd build true Snowpipe auto-ingest with an S3 event notification rather than manual triggers, which I didn't do here purely due to trial account IAM constraints."

### "How is this different from a tutorial project?"

> "I hit and resolved real platform-specific issues that don't show up in tutorials: a pandas 2.x deprecation breaking my date floor function, timezone bugs from server UTC vs IST, a Streamlit HTML rendering issue from a missing `unsafe_allow_html` flag, and the Snowpipe column mismatch. None of those are conceptual gaps — they're the kind of debugging that only surfaces when you actually run something end-to-end rather than copy a working tutorial."

### "What's your testing/validation approach?"

> "For the fraud rules, I validated the overall fraud rate landed near my 10% target by sampling and counting decisions after each change — caught it being 55% versus a wrong account-status weighting early on. For the Snowflake pipeline, I used `COPY_HISTORY` and `TASK_HISTORY` to verify actual row counts and execution states rather than just assuming success from no error message."

---

## Quick Reference — If Asked to Demo Live

1. Open the Streamlit Cloud URL — show the live dashboard, point out auto-refresh and the live fraud alert banner
2. Open GitHub — show the folder structure: `kafka/`, `spark/`, `database/`, `dashboard/`, `finshield_dbt/`
3. If they want Snowflake specifics and you still have trial access, open Snowsight and show `SHOW PIPES`, `SHOW STREAMS`, `SHOW TASKS`, `SHOW DYNAMIC TABLES` — these prove the objects exist and are configured correctly even without re-running everything live
4. If trial has expired, walk through the SQL files in GitHub directly — the code itself is the proof

---

## Things to NOT Overclaim

- Don't say "I built a production fraud detection system" — say "I built a project demonstrating production-pattern fraud detection architecture"
- Don't say "Cortex AI is integrated" — say "Cortex AI's syntax is implemented and documented; live execution requires a paid plan, which I verified by testing"
- Don't say "fully automated pipeline" if Snowpipe ingestion is manually triggered — say "the ingestion pattern matches Snowpipe's mechanics; auto-trigger requires cloud storage event notifications beyond trial account scope"

Honesty about scope under questioning reads as competence, not weakness. Senior interviewers are testing whether you understand what you built, not whether everything is maximally impressive.
