# Achelion ARMS — API Connections & Infrastructure Required
**Last Updated: April 13, 2026**

> All application code is complete. This document lists every external connection
> needed to take ARMS from local development mode to live production.

---

## Current `.env` Status

| Variable            | Status | Value          |
|---------------------|--------|----------------|
| `OPENAI_API_KEY`    | **SET** | sk-proj-...   |
| `DEFAULT_LLM_MODEL` | **SET** | gpt-5.4       |

Everything else below is **NOT YET CONFIGURED** — the system falls back gracefully
to local JSON, in-memory caches, and offline mode for each missing connection.

---

## 1. Broker Connection (IBKR)

Required for: live portfolio data, trade execution, options pricing

| Variable        | Description                   | Default       |
|-----------------|-------------------------------|---------------|
| `IB_HOST`       | TWS/Gateway hostname          | `127.0.0.1`   |
| `IB_PORT`       | TWS/Gateway port              | `4002` (paper) |
| `IB_CLIENT_ID`  | IBKR client ID                | `1`           |

**Setup**: Install TWS or IB Gateway. Enable API connections in TWS settings.
Paper trading port is 4002, live is 4001.

**Modules affected**: `execution/broker_api.py`, `data_feeds/crypto_plugin.py`, `engine/tail_hedge.py`

---

## 2. FRED API (Federal Reserve Economic Data)

Required for: VIX, 10Y Treasury yield, HY credit spread, PMI nowcast

| Variable        | Description                   | Default       |
|-----------------|-------------------------------|---------------|
| `FRED_API_KEY`  | FRED API key                  | *(none)*      |

**Get key**: https://fred.stlouisfed.org/docs/api/api_key.html (free, instant)

**Modules affected**: `data_feeds/fred_plugin.py`

---

## 3. LLM Providers (Intelligence Layer)

Required for: TDC thesis reviews, SENTINEL scanning, Daily Monitor narrative,
Systematic Scan, Proactive Digest

| Variable            | Description                   | Status    |
|---------------------|-------------------------------|-----------|
| `OPENAI_API_KEY`    | OpenAI API key                | **SET**   |
| `DEFAULT_LLM_MODEL` | Model name                   | **SET** (gpt-5.4) |
| `ANTHROPIC_API_KEY` | Anthropic Claude key          | Optional  |
| `GEMINI_API_KEY`    | Google Gemini key             | Optional  |

The LLM wrapper auto-detects provider from model name. Only one provider key
is needed. OpenAI is currently configured and active.

**Modules affected**: `intelligence/llm_wrapper.py`, `engine/tdc.py`,
`engine/systematic_scan.py`, `reporting/daily_monitor.py`, `reporting/proactive_digest.py`

---

## 4. AWS Infrastructure (Production Deployment)

Required for: production scheduling, state backup, PM alerts, database

### 4a. General AWS

| Variable            | Description                   | Default       |
|---------------------|-------------------------------|---------------|
| `AWS_REGION`        | AWS region                    | `us-east-1`   |
| `ARMS_ENVIRONMENT`  | Environment label             | `prod`        |

### 4b. S3 (State Backup)

| Variable              | Description                 | Default                    |
|-----------------------|-----------------------------|----------------------------|
| `ARMS_S3_STATE_BUCKET`| S3 bucket name              | `achelion-arms-state`      |
| `ARMS_S3_BACKUP_PREFIX`| S3 key prefix              | `backups/`                 |

### 4c. SNS (PM Push Alerts)

| Variable              | Description                 | Default       |
|-----------------------|-----------------------------|---------------|
| `ARMS_SNS_ALERT_TOPIC`| SNS topic ARN              | *(none)*      |

### 4d. RDS PostgreSQL

| Variable            | Description                   | Default       |
|---------------------|-------------------------------|---------------|
| `ARMS_PG_HOST`      | RDS hostname                  | *(none — uses JSON fallback)* |
| `ARMS_PG_PORT`      | RDS port                      | `5432`        |
| `ARMS_PG_DATABASE`  | Database name                 | `arms`        |
| `ARMS_PG_USER`      | Database user                 | `arms_app`    |
| `ARMS_PG_PASSWORD`  | Database password             | *(none)*      |
| `ARMS_PG_SSL_MODE`  | SSL mode                      | `require`     |

### 4e. ElastiCache Redis

| Variable            | Description                   | Default       |
|---------------------|-------------------------------|---------------|
| `ARMS_REDIS_HOST`   | Redis hostname                | *(none — uses in-memory fallback)* |
| `ARMS_REDIS_PORT`   | Redis port                    | `6379`        |
| `ARMS_REDIS_DB`     | Redis database number         | `0`           |
| `ARMS_REDIS_PASSWORD`| Redis auth                   | *(none)*      |
| `ARMS_REDIS_SSL`    | Enable TLS                    | `true`        |

**Modules affected**: `infra/db_adapter.py`, `scheduling/master_scheduler.py`

**Terraform**: Infrastructure definitions are in `infra/main.tf`

---

## 5. Vector Knowledge Base (KB Ingest)

Required for: LLM context retrieval from ARMS operational history

| Variable              | Description                 | Default               |
|-----------------------|-----------------------------|-----------------------|
| `ARMS_VECTOR_STORE`   | `pinecone` or `local`      | `local`               |
| `PINECONE_API_KEY`    | Pinecone API key            | *(none — uses local JSON)* |
| `ARMS_PINECONE_INDEX` | Pinecone index name         | `arms-kb`             |
| `PINECONE_ENVIRONMENT`| Pinecone environment        | `us-east-1`           |
| `ARMS_EMBEDDING_MODEL`| OpenAI embedding model      | `text-embedding-3-small` |

**Modules affected**: `intelligence/kb_ingest.py`

---

## 6. Supplementary Data APIs (Anticipatory Intelligence)

Required for: Phase 2.5 anticipatory signals (JPVI, SCCR, etc.)

| Variable            | Description                   | Default       |
|---------------------|-------------------------------|---------------|
| `ADZUNA_APP_ID`     | Adzuna job search API ID      | *(none)*      |
| `ADZUNA_APP_KEY`    | Adzuna job search API key     | *(none)*      |

**Get keys**: https://developer.adzuna.com/ (free tier available)

**Modules affected**: `intelligence/jpvi.py`

---

## 7. SEC EDGAR

Required for: Form 4 insider trade detection, CDM event feeds

| Variable              | Description                 | Default                              |
|-----------------------|-----------------------------|--------------------------------------|
| `ARMS_SEC_USER_AGENT` | SEC EDGAR user-agent string | `Achelion ARMS contact@example.com`  |

SEC requires a valid company name + email in the user-agent header.
No API key needed, but you must identify yourself per SEC fair access policy.

**Modules affected**: `data_feeds/sec_edgar_feed.py`, `data_feeds/news_rss_feed.py`

---

## 8. System Control

| Variable            | Description                            | Default |
|---------------------|----------------------------------------|---------|
| `ARMS_STRICT_LIVE`  | Enforce live data (reject fabrication)  | `1`     |

Set to `0` for development/testing to allow the data pipeline to fall back
to cached values when live feeds are unavailable.

---

## Priority Order for Going Live

1. **FRED_API_KEY** — Free, instant. Enables real macro data pipeline.
2. **IB_HOST/PORT** — Start TWS/Gateway. Enables portfolio + execution.
3. **OPENAI_API_KEY** — Already done.
4. **ARMS_SEC_USER_AGENT** — Update with real company email.
5. **AWS credentials** — For production deployment (S3/SNS/RDS/Redis).
6. **PINECONE_API_KEY** — For production KB (optional, local works for dev).
7. **ADZUNA keys** — For JPVI hiring velocity signals (optional).
