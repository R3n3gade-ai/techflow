# Achelion ARMS — Master Implementation Plan
**Last Updated: April 16, 2026**

> Status: **ALL APPLICATION CODE COMPLETE**. Data feeds rewired to production architecture. EDR advisory integration complete. Only external API key configuration and infrastructure provisioning remain.

---

## System Summary

Achelion ARMS is a $500M+ autonomous hedge fund defense system implementing a 7-layer
risk architecture. The system runs a full daily operational cycle (pre-market sweep,
intraday monitoring, EOD snapshot) across 107 Python modules.

**Architecture AB**: 58% Equity / 20% Crypto / 14% Defensive / 8% Cash

---

## Phase 0: Foundation & Core Logic — COMPLETE

| ID    | Module                          | File                        | Status |
|-------|---------------------------------|-----------------------------|--------|
| P0.01 | Architecture AB Weighting       | `engine/master_engine.py`   | Done   |
| P0.02 | Kevlar Hard Limits (22%/3%)     | `engine/kevlar.py`          | Done   |
| P0.03 | ARAS Regime Assessment          | `engine/aras.py`            | Done   |
| P0.04 | Macro Compass Scoring           | `engine/macro_compass.py`   | Done   |
| P0.05 | Drawdown Sentinel (PDS)         | `engine/drawdown_sentinel.py` | Done |
| P0.06 | Factor Exposure Monitor (FEM)   | `engine/factor_exposure.py` | Done   |
| P0.07 | Master Engine (L4)              | `engine/master_engine.py`   | Done   |

## Phase 1: Intelligence & Automation — COMPLETE

| ID    | Module                          | File                          | Status |
|-------|---------------------------------|-------------------------------|--------|
| P1.01 | MICS Conviction Scoring         | `engine/mics.py`              | Done   |
| P1.02 | SENTINEL Thesis Workflow        | `engine/sentinel_workflow.py` | Done   |
| P1.03 | TDC Thesis Integrity            | `engine/tdc.py`               | Done   |
| P1.04 | CDM Signal Propagation          | `engine/cdm.py`               | Done   |
| P1.05 | CDF Position Decay              | `engine/cdf.py`               | Done   |
| P1.06 | CAM Hedge Sizing                | `engine/cam.py`               | Done   |
| P1.07 | PTRH Tail Hedge Automation      | `engine/tail_hedge.py`        | Done   |
| P1.08 | DSHP Defensive Harvest          | `engine/dshp.py`              | Done   |
| P1.09 | RPE Regime Probability          | `engine/regime_probability.py`| Done   |
| P1.10 | Systematic Scan Engine          | `engine/systematic_scan.py`   | Done   |
| P1.11 | Data Pipeline (FRED/Crypto/PMI) | `data_feeds/pipeline.py`      | Done   |
| P1.12 | IBKR Broker Adapter             | `execution/broker_api.py`     | Done   |
| P1.13 | Universal LLM Wrapper           | `intelligence/llm_wrapper.py` | Done   |
| P1.14 | Audit Log (JSONL)               | `reporting/audit_log.py`      | Done   |
| P1.15 | Confirmation Queue              | `execution/confirmation_queue.py` | Done |
| P1.16 | Daily Monitor v4.0              | `reporting/daily_monitor.py`  | Done   |

## Phase 2: Resilience & Intelligence — COMPLETE

| ID    | Module                          | File                              | Status |
|-------|---------------------------------|-----------------------------------|--------|
| P2.01 | ARES Re-Entry System            | `engine/ares.py`                  | Done   |
| P2.02 | MC-RSS Retail Sentiment         | `engine/mc_rss.py`                | Done   |
| P2.03 | CCM Conviction Calibration      | `engine/conviction_calibration.py`| Done   |
| P2.04 | TRP Thesis Retirement           | `engine/thesis_retirement.py`     | Done   |
| P2.05 | Incapacitation Protocol         | `engine/incapacitation.py`        | Done   |
| P2.06 | ELVT Earnings Language          | `intelligence/elvt.py`            | Done   |
| P2.07 | JPVI Job Posting Velocity       | `intelligence/jpvi.py`            | Done   |
| P2.08 | PFVT Patent Filing              | `intelligence/pfvt.py`            | Done   |
| P2.09 | SCCR Supply Chain               | `intelligence/sccr.py`            | Done   |
| P2.10 | Gate 3 Supplementary Scoring    | `intelligence/gate3_supplementary.py` | Done |

## Phase 3: Platform & Execution — COMPLETE

| ID    | Module                          | File                              | Status |
|-------|---------------------------------|-----------------------------------|--------|
| P3.01 | LAEP Order Book (5-tier VIX)    | `engine/laep.py` + `execution/order_book.py` | Done |
| P3.02 | Circuit Breaker (SPX/VIX)       | `execution/circuit_breaker.py`    | Done   |
| P3.03 | PAIE Integrity Engine           | `engine/paie.py`                  | Done   |
| P3.04 | PERM Covered Call Automation    | `engine/perm.py`                  | Done   |
| P3.05 | AUP Asymmetric Upside           | `engine/asymmetric_upside.py`     | Done   |
| P3.06 | SLOF Leverage Overlay           | `engine/slof.py`                  | Done   |
| P3.07 | Performance Attribution         | `reporting/performance_attribution.py` | Done |
| P3.08 | EOD Snapshot                    | `reporting/eod_snapshot.py`       | Done   |
| P3.09 | Proactive Digest                | `reporting/proactive_digest.py`   | Done   |
| P3.10 | Session Log Analytics           | `engine/session_log_analytics.py` | Done   |

## Phase 4: Operations & Infrastructure — COMPLETE

| ID    | Module                          | File                              | Status |
|-------|---------------------------------|-----------------------------------|--------|
| P4.01 | Correlation Monitor             | `execution/correlation_monitor.py`| Done   |
| P4.02 | Escalation Engine               | `execution/escalation_engine.py`  | Done   |
| P4.03 | Overnight Monitor               | `execution/overnight_monitor.py`  | Done   |
| P4.04 | PM Co-Sign Protocol             | `execution/pm_protocol.py`        | Done   |
| P4.05 | PCR Regime Assessment           | `modules/pcr_regime.py`           | Done   |
| P4.06 | Shutdown Risk Calendar          | `modules/shutdown_risk.py`        | Done   |
| P4.07 | ARAS Sub-Modules (4)            | `modules/deleveraging_risk.py` etc. | Done |
| P4.08 | Stress Scenario Library         | `modules/stress_scenarios.py`     | Done   |
| P4.09 | DB Adapter (Postgres/Redis)     | `infra/db_adapter.py`             | Done   |
| P4.10 | KB Ingest Pipeline              | `intelligence/kb_ingest.py`       | Done   |
| P4.11 | Master Scheduler                | `scheduling/master_scheduler.py`  | Done   |
| P4.12 | Queue Governance                | `execution/queue_*.py`            | Done   |
| P4.13 | Strategic Queue                 | `execution/strategic_queue.py`    | Done   |
| P4.14 | Trade Order Generator           | `execution/trade_order_generator.py` | Done |

---

## What Remains: API Connections & Infrastructure Only

All application logic is written, tested for syntax, and wired into the main orchestration
loop (`main.py`). The system runs in development/offline mode using local JSON fallbacks.

**To go live, the following external connections must be configured in `.env`:**

See `docs/ARMS_API_CONNECTIONS_REQUIRED.md` for the full checklist.

---

## April 16, 2026 — Production Data Feed & EDR Integration Sprint

### Data Feed Architecture (Cleaned)

Removed 4 unnecessary crypto/skew plugins (okx_feed.py, bybit_feed.py, glassnode_feed.py, skew_plugin.py).
Consolidated to 4 production feeds only:

| Feed | Plugin | Signals |
|------|--------|---------|
| FRED API | `data_feeds/fred_plugin.py` | VIX, HY Spread, 10Y Yield, T10Y2Y, Equity PCR, Margin Debt |
| IBKR | `data_feeds/crypto_plugin.py` | CME Futures Basis, OI, Stablecoin Pegs, CBOE SKEW |
| CoinGlass | `data_feeds/coinglass_feed.py` | BTC Funding, OI, Liquidations, Long/Short Ratio, BTC Price |
| ISM PMI | `data_feeds/pmi_plugin.py` | PMI_NOWCAST (CSV bridge — manual monthly update) |

All synthetic fallbacks removed from FRED. No mocks. No temp data except PMI CSV bridge.

### ARAS EDR Advisory Integration (Addendum 7/8)

Wired deleveraging_risk and crypto_microstructure advisory contributions into ARAS:

| Score Range | Advisory Contribution | Regime Pressure |
|-------------|----------------------|-----------------|
| 0.00 – 0.40 | +0.00 | Normal |
| 0.40 – 0.60 | +0.02 | Toward WATCH |
| 0.60 – 0.75 | +0.04 | Toward NEUTRAL |
| 0.75 – 1.00 | +0.06 | Toward DEFENSIVE |

- Max individual: +0.06. Max combined dual-module: +0.12.
- Dual-module alert fires when both > 0.60 (Oct 10 2025 signature).
- `ArasOutput` now includes `dual_edr_alert` and `edr_advisory_total` fields.
- All advisory pressure is upward only — never relaxes the ceiling.

### Files Modified

| File | Change |
|------|--------|
| `data_feeds/pipeline.py` | Rewritten — 4 production feeds only |
| `data_feeds/fred_plugin.py` | Added T10Y2Y + EQUITY_PCR, removed all synthetic fallbacks |
| `data_feeds/pmi_plugin.py` | Rewritten — ISM PMI from CSV bridge |
| `data_feeds/coinglass_feed.py` | Rewritten — single crypto API with long/short + BTC price |
| `data_feeds/crypto_plugin.py` | Added CBOE SKEW fetch via IBKR |
| `engine/aras.py` | EDR advisory contributions + dual-module alert |
| `main.py` | Wired EDR scores into ARAS, added dual-alert logging |

### Files Deleted

| File | Reason |
|------|--------|
| `data_feeds/skew_plugin.py` | CBOE SKEW moved to IBKR crypto_plugin |
| `data_feeds/okx_feed.py` | Consolidated into CoinGlass |
| `data_feeds/bybit_feed.py` | Consolidated into CoinGlass |
| `data_feeds/glassnode_feed.py` | Consolidated into CoinGlass |
| `src/_check_crypto.py` | One-off diagnostic script |

---

## File Counts

| Directory       | Files | Description                             |
|-----------------|------:|-----------------------------------------|
| `engine/`       |    36 | Core risk engines + state persistence   |
| `data_feeds/`   |    12 | Market data pipeline + feed plugins     |
| `execution/`    |    15 | Broker, order book, queue, safety rails |
| `intelligence/` |     8 | LLM wrapper, anticipatory signals, KB   |
| `reporting/`    |     8 | Monitor, snapshot, audit, attribution   |
| `modules/`      |     7 | ARAS sub-modules + stress scenarios     |
| `scheduling/`   |     1 | Master scheduler (ECS/APScheduler)      |
| `infra/`        |     1 | PostgreSQL + Redis adapter              |
| `config/`       |     3 | Configuration constants                 |
| Root            |     2 | `main.py`, `run_daily_report.py`        |
| **Total**       | **93**| **(+ 14 `__init__.py` = 107 files)**    |
