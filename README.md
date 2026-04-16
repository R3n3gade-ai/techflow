# Achelion ARMS v2.0

**Autonomous Risk Management System**
Achelion Capital Management, LLC — Confidential

---

## Overview

ARMS is a fully autonomous hedge fund defense system managing $500M+ AUM across a 7-layer risk architecture. The system executes a complete daily operational cycle — pre-market sweep, intraday monitoring, EOD snapshot — with zero human intervention outside GP-designated veto windows.

**Architecture AB**: 58% Equity / 20% Crypto / 14% Defensive / 8% Cash

---

## System Status — April 16, 2026

| Category | Status |
|----------|--------|
| Application Code | **118 Python modules — ALL COMPLETE** |
| Data Feeds | **Production — FRED, IBKR, CoinGlass, ISM PMI** |
| ARAS + EDR Integration | **Complete — Addendum 7/8 wired** |
| Backtester | **Phase 1 + Phase 2 — Operational** |
| Infrastructure (Terraform) | Defined — pending deployment |
| Live Broker Connection | IBKR adapter built — pending Gateway config |

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  MAIN ORCHESTRATOR               │
│              src/main.py (7-phase cycle)         │
├─────────────────────────────────────────────────┤
│  L1: DATA FEEDS (The Senses)                    │
│    FRED API → VIX, HY Spread, 10Y, T10Y2Y,     │
│               PCR, Margin Debt                   │
│    IBKR     → CME Futures Basis, OI, Stablecoin │
│               Pegs, CBOE SKEW                    │
│    CoinGlass→ Funding, OI, Liquidations,         │
│               Long/Short, BTC Price              │
│    ISM PMI  → CSV Bridge (manual monthly)        │
├─────────────────────────────────────────────────┤
│  L2: MACRO COMPASS                              │
│    VIX 30% + HY 30% + PMI 20% + 10Y 20%        │
│    + Typed Macro Event Overlay                   │
├─────────────────────────────────────────────────┤
│  L3: ARAS (Regime → Equity Ceiling)             │
│    5 Regimes: RISK_ON → WATCH → NEUTRAL →       │
│               DEFENSIVE → CRASH                  │
│    Hysteresis ±0.05 + NEUTRAL persistence        │
│    EDR Advisory: Delev + CryptoMicro (max +0.12)│
│    Dual-Module Alert when both > 0.60            │
├─────────────────────────────────────────────────┤
│  L4: MASTER ENGINE (Target Weights)             │
│    MICS conviction scoring, Kevlar 22% cap,      │
│    SENTINEL thesis workflow                      │
├─────────────────────────────────────────────────┤
│  EXECUTION LAYER                                │
│    IBKR Broker, LAEP 5-tier VIX order book,     │
│    Circuit breaker, Confirmation queue           │
└─────────────────────────────────────────────────┘
```

---

## Production Data Feed Architecture

| Feed | Source | Signals | Auth |
|------|--------|---------|------|
| **FRED** | FRED API | VIX, HY Spread, 10Y Yield, T10Y2Y, Equity PCR, Margin Debt | `FRED_API_KEY` |
| **IBKR** | IB Gateway | CME Futures Basis, OI, Stablecoin Pegs, CBOE SKEW | IB Gateway |
| **CoinGlass** | Public API | BTC Funding, OI, Liquidations, Long/Short Ratio, BTC Price | Free (no auth) |
| **ISM PMI** | CSV Bridge | PMI_NOWCAST | Manual monthly update |

No mocks. No synthetic fallbacks. All feeds are production except PMI (CSV bridge until production API selected).

---

## Module Inventory (118 files)

| Directory | Count | Purpose |
|-----------|------:|---------|
| `engine/` | 36 | Core risk engines, state persistence, conviction scoring |
| `data_feeds/` | 11 | Market data pipeline + 4 production feed plugins |
| `execution/` | 15 | Broker adapter, order book, queues, safety rails |
| `intelligence/` | 8 | LLM wrapper, ELVT, JPVI, PFVT, SCCR, Gate 3 |
| `reporting/` | 8 | Daily monitor, EOD snapshot, audit log, attribution |
| `modules/` | 7 | ARAS sub-modules (EDR) + stress scenarios |
| `simulation/` | 7 | Backtester Phase 1 + Phase 2 engines |
| `scheduling/` | 1 | Master scheduler (ECS/APScheduler) |
| `infra/` | 1 | PostgreSQL + Redis adapter |
| `config/` | 3 | Configuration constants |

---

## Addendum Status

| # | Title | Module | Status |
|---|-------|--------|--------|
| 1 | PTRH + DSHP | `engine/tail_hedge.py`, `engine/dshp.py` | Complete |
| 2 | CDM + TDC | `engine/cdm.py`, `engine/tdc.py` | Complete |
| 3 | Intelligence Phase 2/3 | `intelligence/elvt.py`, `jpvi.py`, `pfvt.py`, `sccr.py` | Complete |
| 4 | CAM Hedge Sizing | `engine/tail_hedge.py` (integrated) | Complete |
| 5 | SEM Automation | `scheduling/master_scheduler.py` | Complete |
| 6 | PTRH Adaptive Strike | `engine/tail_hedge.py` | Complete |
| 7 | **Deleveraging Risk (EDR)** | `modules/deleveraging_risk.py` | **Complete — wired into ARAS** |
| 8 | **Crypto Microstructure (EDR)** | `modules/crypto_microstructure.py` | **Complete — wired into ARAS + dual-alert** |

---

## Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | Full 7-phase ARMS orchestration cycle |
| `src/engine/aras.py` | ARAS regime assessor with EDR advisory integration |
| `src/engine/macro_compass.py` | L2 macro regime scoring |
| `src/data_feeds/pipeline.py` | Production data pipeline (4 feeds) |
| `src/run_backtest.py` | Backtester entry point |
| `src/run_daily_report.py` | Standalone daily report runner |
| `MASTER_IMPLEMENTATION_PLAN.md` | Detailed module-by-module build status |
| `CODEBASE_MAP.md` | Full file tree with descriptions |

---

## Running

```bash
# Prerequisites: Python 3.12, IB Gateway running, .env configured
# See docs/ARMS_API_CONNECTIONS_REQUIRED.md for full checklist

# Full ARMS cycle
cd src && python main.py

# Backtest
cd src && python run_backtest.py

# Daily report only
cd src && python run_daily_report.py
```

---

## Repository Structure

```
techflow/
├── .env                     # API keys (gitignored)
├── .gitignore
├── README.md                # This file
├── MASTER_IMPLEMENTATION_PLAN.md
├── CODEBASE_MAP.md
├── data/                    # Bridge files, templates, original specs
├── docs/                    # Architecture docs, audits, specs
├── infra/                   # Terraform (ECS/RDS/Redis/S3)
├── SAMPLES/                 # Backtest reports and tearsheets
├── src/                     # All application code (118 .py files)
├── state/                   # Persistent state files
├── system_map/              # Interactive architecture visualization
└── tasks/                   # Development task tracking
```

---

*Achelion Capital Management, LLC — Flow. Illumination. Discipline. Conviction.*
