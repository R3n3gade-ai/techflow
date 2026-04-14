# ACHELION ARMS — CLAUDE.md
# Architectural Context File · v4.0 · March 2026
# Read this file at the start of every development session.
# This file is the single source of truth for system architecture.
# Last updated: March 28, 2026 — corrected compensation terms, regime thresholds,
# PTRH CRASH multiplier, and added Addenda 1-4 modules to file structure.

---

## FUND CONTEXT

**Achelion Capital Management, LLC**
- PM / Architect: MJ Pence
- Lead Developer: Josh Paul
  - Cash: $15,000 lump sum paid April 1, 2026
  - Equity: 10% AT LLC membership interest, 4-year vest, 1-year cliff
- GPs: Brandon, James (active); Crystal, MJ join upon full-time transition
- MJ holds a securities license at a third-party firm — MJ has NO current legal or
  internet-visible connection to Achelion during the bridge period. All AT LLC ownership
  is held by Achelion Holdings Co LLC. Do not reference MJ as an owner in any code
  comment, commit message, or document that leaves this repository.
- Fund thesis: concentrated AI infrastructure
- Goal: license ARMS to other hedge funds via Achelion Technology LLC (3-5yr horizon)
- AUM target: $50M at full deployment

**Portfolio Allocation — Architecture AB v4.0**
- 58% Equity (AI infrastructure concentrated: NVDA, AMD, ALAB, MU, MRVL, AVGO, ANET, ARM, PLTR, TSLA, VRT, ETN)
- 20% Crypto (IBIT 12% / ETHB 4% / BSOL 4%)
- 14% Defense — EXEMPT from exposure ceiling (SGOV 3% / SGOL 2% / DBMF 5% / STRC 4%)
- 8% Cash — EXEMPT from exposure ceiling (core hedge 1.2% / regime reserve STRC 2.0% / ops buffer 4.8%)
- PTRH (QQQ puts) — EXEMPT from exposure ceiling, permanent structural hedge

**Primary benchmark:** S&P 500 (SPY)

---

## SYSTEM OVERVIEW

ARMS = Achelion Risk Management System
Version: v4.0 + Addenda 1-4
Language: Python 3.11+
Database: SQLite (dev) → PostgreSQL (prod)
ORM: SQLAlchemy
Config: YAML via fund-agnostic config layer
Testing: pytest

**Seven Pillars:**
1. ARAS — Aggregated Risk Assessment System (regime classifier, HIGHEST AUTHORITY)
2. Macro Compass — macroeconomic signal aggregator
3. Master Engine — portfolio construction and conviction weighting
4. Kevlar — position-level risk controls and concentration limits
5. PERM — portfolio evolution and rebalancing manager
6. SLOF — systematic long overlay framework (conviction overlays)
7. ARES — automated re-entry and exit system

**v4.0 Seven Gap Upgrades (new modules):**
- GAP 1: FEM — Factor Exposure Monitor (src/modules/factor_exposure.py)
- GAP 2: VARES — Volatility-Adjusted Re-entry Sizing (extends src/engine/ares.py)
- GAP 3: PDS — Portfolio Drawdown Sentinel (src/engine/drawdown_sentinel.py)
- GAP 4: LAEP — Liquidity-Adjusted Execution Protocol (extends src/execution/order_book.py)
- GAP 5: PTRH — Permanent Tail Risk Hedge (src/engine/tail_hedge.py)
- GAP 6: CDF — Conviction Decay Function (extends src/engine/perm.py)
- GAP 7: SSL — Stress Scenario Library (src/modules/stress_scenarios.py)

**Addendum 1 — PTRH Automation + DSHP:**
- Module A: PTRH Full Tier 0 Automation (src/engine/tail_hedge.py — UPDATE)
- Module B: Defensive Sleeve Harvest Protocol (src/engine/dshp.py — NEW)

**Addendum 2 — CDM + TDC (thesis integrity layer):**
- Module C: Customer Dependency Map (src/engine/cdm.py — NEW)
- Module D: Thesis Dependency Checker (src/engine/tdc.py — NEW)
- Config: src/config/position_dependency_map.py — NEW
- Config: src/config/dshp_config.py — NEW

**Addendum 3 — Intelligence Architecture Phase 2 & 3:**
- ELVT: Earnings Language Velocity Tracker (src/intelligence/elvt.py — NEW)
- JPVI: Job Posting Velocity Intelligence (src/intelligence/jpvi.py — NEW)
- PFVT: Patent Filing Velocity Tracker (src/intelligence/pfvt.py — NEW)
- SCCR: Supply Chain Cross-Reference (src/intelligence/sccr.py — NEW)
- Claude API wrapper (src/intelligence/claude_wrapper.py — NEW)

**Addendum 4 — Governing Principle + CAM:**
- CAM: Coverage Adequacy Model (src/engine/cam.py — NEW)
  - Tier 0 autonomous PTRH sizing. Runs every 5 min.
  - After CAM is live, PTRH NEVER appears in PM decision queue.

**Reporting and delivery (Infrastructure Spec + EOD Snapshot Spec):**
- Daily monitor (src/reporting/daily_monitor.py — NEW)
- EOD Snapshot (src/reporting/eod_snapshot.py — NEW)
- Delivery pipeline (src/reporting/delivery.py — NEW)
- Confirmation queue (src/execution/confirmation_queue.py — NEW)
- Broker API layer (src/execution/broker_api.py — NEW)
- Knowledge base (src/intelligence/knowledge_base.py — NEW)

---

## THE GOVERNING PRINCIPLE — READ THIS FIRST

> "The PM needs to be at the lunch. The system needs to be running the portfolio."

The PM's edge is physical presence in rooms where the future is decided before it enters
any dataset. The system executes everything decided by math, process, and data inflow.

**Before building any feature, ask:**
Is this decision based on math, process, and data inflow?
  → YES: Automate it. Tier 0. No PM involvement. No confirmation window.
  → NO (requires pre-consensus human intelligence): Preserve the touchpoint. Surface it
     precisely. Make the PM's response frictionless.

A recurring decision queue item that requires the same PM action every day is not a
safeguard. It is evidence of an incomplete build.

**Two legitimate human touchpoints — everything else is automated:**
1. SENTINEL thesis seeding (Gate 6 source declaration)
2. TDC IMPAIRED/BROKEN response (Category A intelligence gate)

---

## AUTHORITY HIERARCHY — IMMUTABLE

This is the most critical architectural rule. Never violate it.

```
ARAS ceiling          → ABSOLUTE. No module, human, or override can exceed it.
PDS ceiling           → ADDITIVE. min(ARAS_ceiling, PDS_ceiling) always prevails.
                        PDS can only make portfolio MORE defensive, never less.
CAM                   → TIER 0. Autonomous PTRH sizing. No PM involvement.
FEM                   → ADVISORY only. No ceiling authority.
PTRH                  → ADDITIVE (outside ceiling calculation entirely).
PM override           → Can override PDS with documented justification + GP co-sign.
                        CANNOT override ARAS under any circumstances.
```

**Effective ceiling formula (run every session):**
```python
effective_ceiling = min(aras_output.exposure_ceiling, pds_output.pds_ceiling)
```

---

## REGIME DEFINITIONS — v4.0 CANONICAL

```
RISK_ON    composite < 0.30   ceiling: 100%   SLOF: active    PTRH: 1.0×   base 1.2% NAV
WATCH      0.30–0.50          ceiling: 100%   SLOF: active    PTRH: 1.25×  base 1.5% NAV
NEUTRAL    0.51–0.65          ceiling: 75%    SLOF: reduce    PTRH: 1.25×  base 1.5% NAV
DEFENSIVE  0.66–0.80          ceiling: 40%    SLOF: remove    PTRH: 1.5×   base 1.8% NAV
CRASH      > 0.80             ceiling: 15%    SLOF: remove    PTRH: 2.0×   base 2.4% NAV
```

**CRASH note:** In CRASH regime, CAM auto-corrects PTRH to 2.0× minimum. This is
autonomous — CAM handles it. Do NOT implement "no new buys" logic from earlier specs.
The CAM spec (Addendum 4) supersedes all prior PTRH CRASH behavior.

**Hysteresis:** 0.35 (upward) / 0.25 (downward) — prevents whipsaw
**Persistence:** 2-session NEUTRAL confirmation before escalation

**Escalation Rule v2 (post-cut escalation):**
- Fires when: 2 consecutive sessions of DEFENSIVE decline post any regime cut
- Auto-suppression: if composite is DECREASING session-over-session, escalation is cancelled
- Auto-suppression is evaluated fresh each session — does NOT carry across sessions

---

## FILE STRUCTURE — COMPLETE (including Addenda 1-4)

```
achelion-arms/
├── CLAUDE.md                              ← THIS FILE
├── README.md
├── requirements.txt
├── config/
│   ├── base_config.yaml                   ← fund-agnostic defaults
│   └── achelion_config.yaml               ← Achelion-specific overrides
├── src/
│   ├── __init__.py
│   ├── config/                            ← NEW (Addendum 2)
│   │   ├── position_dependency_map.py     ← CDM named entity map (PM-maintained)
│   │   └── dshp_config.py                 ← DSHP threshold constants
│   ├── dataclasses/                       ← ALL dataclasses live here
│   │   ├── __init__.py
│   │   ├── regime.py
│   │   ├── portfolio.py
│   │   ├── signals.py
│   │   ├── execution.py
│   │   ├── risk_v40.py                    ← ALL v4.0 dataclasses
│   │   └── reporting.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── aras.py                        ← ARAS composite
│   │   ├── macro_compass.py               ← macro signal aggregator
│   │   ├── master_engine.py               ← portfolio construction
│   │   ├── kevlar.py                      ← position-level risk controls
│   │   ├── perm.py                        ← PERM + CDF conviction decay
│   │   ├── slof.py                        ← systematic long overlay
│   │   ├── ares.py                        ← ARES + VARES vol-adjusted re-entry
│   │   ├── drawdown_sentinel.py           ← PDS
│   │   ├── tail_hedge.py                  ← PTRH (Tier 0 via Addendum 1)
│   │   ├── dshp.py                        ← NEW (Addendum 1): Defensive Sleeve Harvest
│   │   ├── cdm.py                         ← NEW (Addendum 2): Customer Dependency Map
│   │   ├── tdc.py                         ← NEW (Addendum 2): Thesis Dependency Checker
│   │   └── cam.py                         ← NEW (Addendum 4): Coverage Adequacy Model
│   ├── modules/                           ← ARAS sub-modules
│   │   ├── __init__.py
│   │   ├── deleveraging_risk.py
│   │   ├── crypto_microstructure.py
│   │   ├── margin_stress.py
│   │   ├── dealer_gamma.py
│   │   ├── pcr_regime.py
│   │   ├── shutdown_risk.py
│   │   ├── factor_exposure.py             ← FEM
│   │   └── stress_scenarios.py            ← SSL
│   ├── intelligence/                      ← NEW (Addendum 3 + Infrastructure Spec)
│   │   ├── __init__.py
│   │   ├── claude_wrapper.py              ← Claude API integration layer
│   │   ├── knowledge_base.py              ← Chroma DB interface
│   │   ├── elvt.py                        ← Earnings Language Velocity Tracker
│   │   ├── jpvi.py                        ← Job Posting Velocity Intelligence
│   │   ├── pfvt.py                        ← Patent Filing Velocity Tracker
│   │   └── sccr.py                        ← Supply Chain Cross-Reference
│   ├── execution/
│   │   ├── __init__.py
│   │   ├── circuit_breaker.py
│   │   ├── order_book.py                  ← LAEP liquidity-adjusted execution
│   │   ├── overnight_monitor.py
│   │   ├── correlation_monitor.py
│   │   ├── escalation_engine.py
│   │   ├── trade_order_generator.py
│   │   ├── pm_protocol.py
│   │   ├── broker_api.py                  ← NEW: sole IBKR interface
│   │   └── confirmation_queue.py          ← NEW: Tier 1 veto window queue
│   ├── reporting/                         ← NEW (Infrastructure Spec + EOD Snapshot)
│   │   ├── __init__.py
│   │   ├── daily_monitor.py               ← 6AM CT monitor generation
│   │   ├── eod_snapshot.py                ← 1455 CT EOD snapshot (5 fields)
│   │   └── delivery.py                    ← email + web dashboard delivery
│   ├── data_feeds/
│   │   ├── __init__.py
│   │   ├── fred_feed.py
│   │   ├── binance_feed.py
│   │   ├── yahoo_feed.py
│   │   └── feed_resilience.py
│   └── api/
│       ├── __init__.py
│       └── dashboard_api.py
├── db/
│   ├── __init__.py
│   ├── models.py
│   └── migrations/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── __init__.py
│   │   └── market_data.py
│   ├── test_authority_hierarchy.py        ← CRITICAL: run before/after every engine change
│   ├── test_circuit_breakers.py
│   ├── test_regime_transitions.py
│   ├── test_v40_dataclasses.py
│   ├── test_v40_modules.py
│   ├── test_cam.py                        ← NEW: CAM coverage adequacy tests
│   ├── test_cdm_tdc.py                    ← NEW: CDM/TDC thesis integrity tests
│   └── test_dshp.py                       ← NEW: DSHP harvest trigger tests
└── scripts/
    ├── daily_run.py
    └── backtest_runner.py
```

---

## DATABASE TABLES

**Existing (v3.1):**
- `regime_log` — daily regime outputs
- `composite_scores` — ARAS component scores
- `position_targets` — Master Engine outputs
- `circuit_breaker_log` — CB firings
- `session_log` — PM decisions and documentation
- `lp_narratives` — auto-generated LP communications
- `reentry_plans` — ARES re-entry tracking

**New in v4.0:**
- `factor_exposure_log` — daily FEM snapshots
- `drawdown_sentinel_log` — NAV vs HWM tracking
- `tail_hedge_positions` — QQQ put position ledger
- `scenario_pnl_log` — daily SSL scenario outputs

**New in Addenda 1-4:**
- `dshp_harvest_log` — defensive sleeve harvest actions
- `cdm_event_log` — named entity alerts and propagation records
- `tdc_review_log` — thesis integrity scores per position per review
- `cam_action_log` — CAM PTRH auto-correction events
- `confirmation_queue` — Tier 1 veto window items
- `eod_snapshot_log` — EOD snapshot generation records

---

## DATACLASS REGISTRY — v4.0

All v4.0 dataclasses live in `src/dataclasses/risk_v40.py`.

**Implemented:**
- `LiquidityMode` (Enum)
- `FactorExposure`
- `FactorExposureSignal`
- `DrawdownSentinelSignal`
- `ReentryPlan`
- `OptionsPosition`
- `TailHedgeStatus`
- `ConvictionDecayInfo`
- `ScenarioPnL`
- `ScenarioResults`
- `PositionTarget` (extended: conviction_decay_factor, effective_c_squared)
- `OrderBookEntry` (extended: liquidity_mode, order_type, execution_window_min)

**To add for Addenda 1-4:**
- `HarvestAction` — DSHP harvest event
- `CDMAlert` — named entity propagation signal
- `ThesisReviewResult` — TDC thesis integrity score
- `TDCStatus` — TDC module state
- `CAMResult` — Coverage Adequacy Model output
- `ConfirmationQueueItem` — Tier 1 action
- `EODSnapshotOutput` — EOD snapshot five-field structure

---

## KEY THRESHOLDS — CANONICAL (Addenda supersede earlier values)

```python
# ARAS Composite thresholds — CANONICAL v4.0
COMPOSITE_RISK_ON_MAX    = 0.30   # was 0.25 in skeleton — CORRECTED
COMPOSITE_WATCH_MAX      = 0.50   # was 0.35 in skeleton — CORRECTED
COMPOSITE_NEUTRAL_MAX    = 0.65   # was 0.50 in skeleton — CORRECTED
COMPOSITE_DEFENSIVE_MAX  = 0.80   # was 0.70 in skeleton — CORRECTED
# CRASH = composite > 0.80        # was >= 0.70 — CORRECTED

# Hysteresis
HYSTERESIS_UP   = 0.35
HYSTERESIS_DOWN = 0.25

# Factor Exposure Monitor
FEM_WATCH_THRESHOLD  = 0.65
FEM_ALERT_THRESHOLD  = 0.80
FEM_CORR_WARN        = 0.70

# Portfolio Drawdown Sentinel
PDS_WARN_PCT        = -0.08
PDS_DELEVERAGE_1    = -0.12   # -12% from HWM = 60% ceiling
PDS_DELEVERAGE_2    = -0.18   # -18% from HWM = 30% ceiling
PDS_CEIL_NORMAL     =  1.00
PDS_CEIL_DELEV_1    =  0.60
PDS_CEIL_DELEV_2    =  0.30

# VARES
VARES_VIX_LOOKBACK  = 90
VARES_MIN_TRANCHE   = 0.15
VARES_MAX_TRANCHE   = 0.35
VARES_TRANCHES      = 3
VARES_HOURS_BETWEEN = 48

# Conviction Decay Function (CDF)
CDF_TRIGGER_DAYS    = 45
CDF_TRIGGER_GAP     = -0.10
CDF_DECAY_45D       = 0.80
CDF_DECAY_90D       = 0.60
CDF_REVIEW_DAYS     = 135
CDF_RESET_OUTPERFORM = 0.05
CDF_RESET_DAYS      = 15
# INSIDER SALE: triggers 21-day accelerated CDF window (CDM event type)

# LAEP
LAEP_NORMAL_VIX_MAX   = 25
LAEP_ELEVATED_VIX_MAX = 45
LAEP_NORMAL_WINDOW_MIN   = 30
LAEP_ELEVATED_WINDOW_MIN = 60
LAEP_CRISIS_WINDOW_MIN   = 90
LAEP_NORMAL_SLIPPAGE_BPS   =  8
LAEP_ELEVATED_SLIPPAGE_BPS = 20
LAEP_CRISIS_SLIPPAGE_BPS   = 40

# PTRH — regime multipliers (CAM handles sizing autonomously)
PTRH_BASE_NAV_PCT    = 0.012   # 1.2% of NAV = base notional
PTRH_MULT_RISK_ON    = 1.00    # 1.2% NAV
PTRH_MULT_WATCH      = 1.25    # 1.5% NAV
PTRH_MULT_NEUTRAL    = 1.25    # 1.5% NAV
PTRH_MULT_DEFENSIVE  = 1.50    # 1.8% NAV
PTRH_MULT_CRASH      = 2.00    # 2.4% NAV
PTRH_ROLL_DTE        = 30      # roll when DTE reaches 30

# PTRH — strike, delta, DTE specification (CANONICAL — updated March 31, 2026)
# Rationale: 5–8% OTM maximizes convexity at the strikes where real drawdowns land.
# ATM overpays for protection the defensive sleeve already covers (first 5% move).
# 15–20% OTM requires catastrophic move before meaningful intrinsic value — lottery tickets.
# 5–8% OTM at delta –0.30 to –0.40 is the professional tail hedge standard
# (Universa / Spitznagel convexity model). Gamma accelerates as portfolio drawdown
# approaches and breaches the strike — maximum payoff where it is most needed.
PTRH_STRIKE_OTM_MIN  = 0.05   # 5% OTM floor
PTRH_STRIKE_OTM_MAX  = 0.08   # 8% OTM ceiling
PTRH_STRIKE_TARGET   = 0.065  # 6.5% OTM target (midpoint)
PTRH_DELTA_MIN       = -0.40  # delta floor (more negative = deeper OTM)
PTRH_DELTA_MAX       = -0.30  # delta ceiling (less negative = closer to ATM)
PTRH_DELTA_TARGET    = -0.35  # target delta at execution
PTRH_DTE_MIN         = 60     # minimum DTE at entry
PTRH_DTE_MAX         = 90     # maximum DTE at entry
PTRH_DTE_TARGET      = 75     # target DTE (midpoint)
PTRH_ANNUAL_COST_PCT = 0.008  # ~0.80% NAV/yr at 5–8% OTM (vs 1.5–2.0% ATM)
# CAM auto-corrects notional every 5 min. 5% tolerance to add, 15% to reduce.

# CAM — Coverage Adequacy Model (Addendum 4)
CAM_BASE_COVERAGE_PCT       = 0.012   # 1.2% NAV floor
CAM_CORRECTION_TOLERANCE    = 0.05    # auto-correct if >5% short
CAM_REDUCTION_TOLERANCE     = 0.15    # asymmetric: only reduce if >15% over
CAM_RUN_INTERVAL_MINUTES    = 5
CAM_MAX_COVERAGE_PCT        = 0.035   # 3.5% NAV ceiling

# DSHP — Defensive Sleeve Harvest Protocol (Addendum 1)
SGOL_TARGET_WEIGHT        = 0.020
SGOL_HARVEST_THRESHOLD    = 0.200
DBMF_TARGET_WEIGHT        = 0.050
DBMF_HARVEST_THRESHOLD    = 0.150
DBMF_DRIFT_THRESHOLD      = 0.015
DSHP_VETO_WINDOW_HOURS    = 4.0
DSHP_VETO_GP_ALERT_COUNT  = 2

# CDM — Customer Dependency Map (Addendum 2)
CDM_FORM4_THRESHOLD_USD        = 50000   # open-market C-suite sale threshold
CDM_FORM4_CDF_ACCEL_DAYS       = 21      # accelerated CDF window on insider sale
CDM_TDC_REVIEW_HOURS_CRITICAL  = 6       # TDC review within 6h of CRITICAL event
CDM_TDC_REVIEW_HOURS_HIGH      = 24      # TDC review within 24h of HIGH event

# TDC — Thesis Integrity Score thresholds (Addendum 2)
TIS_INTACT_MIN   = 8.0    # 8.0–10.0 = INTACT
TIS_WATCH_MIN    = 6.0    # 6.0–7.9 = WATCH
TIS_IMPAIRED_MIN = 4.0    # 4.0–5.9 = IMPAIRED → PM review queued
# 0.0–3.9 = BROKEN → CDF accelerated + SENTINEL full re-run

# Transaction cost model
TCM_NORMAL_BPS   =  8
TCM_ELEVATED_BPS = 20
TCM_CRISIS_BPS   = 40
```

---

## CRITICAL DESIGN RULES — READ BEFORE EVERY SESSION

1. **ARAS ceiling is absolute.** No function may return exposure above `aras_output.exposure_ceiling`.

2. **PDS is independent.** `drawdown_sentinel.py` must never import from `aras.py`. Peers. Ceiling computed in `master_engine.py` via `min()`.

3. **FEM is advisory only.** Max +0.05 advisory_composite_add. ARAS decides.

4. **PTRH is outside ceiling math.** Never included in gross exposure calculations.

5. **CDF does not force sells.** Only reduces `effective_c_squared`. Position stays in book.

6. **LAEP priority reorder in CRISIS.** CRISIS execution order: BSOL → ETHB → IBIT → equity (least liquid first). Opposite of normal. Test explicitly.

7. **Auto-suppression is session-scoped.** Runs fresh every session. Does not carry state.

8. **HWM never decrements.** `max(current_hwm, today_nav)` always.

9. **CAM owns PTRH sizing.** After CAM is live, PTRH never appears in PM decision queue. Only exception: broker API execution failure. CAM runs every 5 min. Asymmetric tolerance: 5% to add coverage, 15% to reduce.

10a. **PTRH strike is 5–8% OTM.** Not ATM. Not 15–20% OTM. The 5–8% OTM range is the convexity sweet spot — options respond meaningfully to real drawdowns without overpaying for protection the defensive sleeve already provides. CAM sizes notional; tail_hedge.py selects the compliant strike. Any strike outside 5–8% OTM is a spec violation regardless of liquidity rationale.

10. **TDC never executes trades.** TDC surfaces a question. The PM answers it (or silences, which is logged as confirmation). TDC is advisory on thesis integrity only.

11. **CDM Form 4 insider sales.** CEO/CFO open-market sales >$50K trigger HIGH CDM alert + 21-day CDF acceleration. Exclude 10b5-1 pre-planned sales.

12. **EOD Snapshot is one page.** Five fields only: regime delta, pending Tier 1, intraday CDM/TDC signals, session execution summary, overnight watch statement. Generated at 1450 CT, delivered 1455 CT.

13. **All monetary values in USD.** All percentages as floats (0.58 not 58). All dates as ISO 8601.

14. **No code from third parties without approved license.** All code must be original, AT LLC-provided, or licensed under MIT/Apache 2.0/BSD/ISC. GPL/LGPL/AGPL require prior written approval. Maintain dependency register.

---

## DELIVERY SCHEDULE

```
0530 CT — Daily monitor generated (daily_monitor.py)
0600 CT — Daily monitor delivered to PM + GPs (delivery.py)
0800 CT — PM reads morning monitor
1450 CT — EOD Snapshot generated (eod_snapshot.py)
1455 CT — EOD Snapshot delivered to PM + GPs
2000 CT — Knowledge base nightly ingest (knowledge_base.py)
2030 CT — PostgreSQL backup (pg_dump)
```

---

## DATA FEEDS

| Feed    | Source    | Used For                              | Fallback              |
|---------|-----------|---------------------------------------|-----------------------|
| FRED    | FRED API  | HY OAS, 10Y yield, net liquidity      | Prior day cached      |
| Binance | REST API  | BTC/ETH funding rates, price          | CoinGecko public API  |
| Yahoo   | yfinance  | QQQ, IBIT, ETHB, BSOL, equity prices | Prior day cached      |
| VIX     | Yahoo/CBOE| Volatility index                      | Cached + interpolated |
| NewsAPI | REST API  | CDM named entity monitoring           | EDGAR RSS             |
| EDGAR   | SEC REST  | Form 4 insider sale filings           | No fallback — flag    |
| Adzuna  | REST API  | JPVI job posting velocity             | LinkedIn public       |
| USPTO   | PatentsView API | PFVT patent filing velocity     | Monthly bulk download |

Staleness threshold: 4 hours intraday. Flag stale feeds in monitor output.

---

## VALIDATION TARGET — OCTOBER 10, 2025

Canonical system validation test. ARMS must demonstrate 4-day advance warning.
Composite must cross into DEFENSIVE by October 6, 2025.
All backtest work validated against this event first.

---

## CURRENT BUILD STATUS

| Component                    | Status      | Notes                                      |
|------------------------------|-------------|------------------------------------------- |
| v3.1 seven pillars           | ✓ Specified | Architecture complete, needs live feeds    |
| All v4.0 dataclasses         | ✓ Stubbed   | See src/dataclasses/risk_v40.py            |
| FEM (Gap 1)                  | ◐ Stubbed   | Interface defined, logic to build          |
| VARES (Gap 2)                | ◐ Stubbed   | Interface defined, logic to build          |
| PDS (Gap 3)                  | ◐ Stubbed   | Interface defined, logic to build          |
| LAEP (Gap 4)                 | ◐ Stubbed   | Interface defined, logic to build          |
| PTRH (Gap 5)                 | ◐ Stubbed   | Interface defined, logic to build          |
| CDF (Gap 6)                  | ◐ Stubbed   | Interface defined, logic to build          |
| SSL (Gap 7)                  | ◐ Stubbed   | Interface defined, logic to build          |
| DSHP (Addendum 1)            | ○ Pending   | Stub file created — logic to build         |
| PTRH Tier 0 (Addendum 1)     | ○ Pending   | tail_hedge.py update required              |
| CDM (Addendum 2)             | ○ Pending   | Stub file created — logic to build         |
| TDC (Addendum 2)             | ○ Pending   | Stub file created — logic to build         |
| position_dependency_map.py   | ○ Pending   | Config stub created — PM to review/confirm |
| CAM (Addendum 4)             | ○ Pending   | Stub file created — logic to build         |
| Claude API wrapper           | ○ Pending   | Stub file created — logic to build         |
| Knowledge base (Chroma)      | ○ Pending   | Stub file created — logic to build         |
| ELVT (Addendum 3)            | ○ Pending   | Stub file created — logic to build         |
| JPVI (Addendum 3)            | ○ Pending   | Stub file created — logic to build         |
| PFVT (Addendum 3)            | ○ Pending   | Stub file created — logic to build         |
| SCCR (Addendum 3)            | ○ Pending   | Stub file created — logic to build         |
| Daily monitor                | ○ Pending   | Stub file created — logic to build         |
| EOD Snapshot                 | ○ Pending   | Stub file created — logic to build         |
| Confirmation queue           | ○ Pending   | Stub file created — logic to build         |
| Broker API layer             | ○ Pending   | Stub file created — logic to build         |
| Database models (Addenda)    | ○ Pending   | New tables to add to db/models.py          |
| IBKR paper trading           | ○ Pending   | Requires broker_api.py + 30-day validation |
| Oct 10 2025 validation       | ○ Pending   | Requires live feed completion              |

**Build priority sequence (Phase 1):**
1. MICS formula — highest priority. Foundation for everything.
2. Free signal feeds + CDM config population (1 day)
3. CDM + TDC (1 week) — closes thesis integrity gap
4. CAM (2-3 days) — PTRH fully autonomous
5. Daily monitor + EOD Snapshot (1 week) — PM visibility
6. IBKR paper connection + 30-day validation
7. DSHP (1-2 days)

Legend: ✓ Complete  ◐ In progress  ○ Not started

---

## SESSION STARTUP CHECKLIST

- [ ] Read this CLAUDE.md file in full
- [ ] Identify which file(s) are being worked on today
- [ ] Confirm the authority hierarchy is understood
- [ ] If modifying ARAS: does the change respect absolute ceiling authority?
- [ ] If modifying execution: does LAEP crisis priority reorder correctly?
- [ ] If modifying PDS: is it still independent from ARAS?
- [ ] If modifying PTRH/tail_hedge: does CAM own the sizing? No PM touchpoint?
- [ ] Run `pytest tests/test_authority_hierarchy.py` before and after any engine change

---

## CONTACT / REPO

Project: achelion-arms
Lead Developer: Josh Paul
Architect: MJ (via Achelion Holdings Co LLC) + Claude (Anthropic)
All architecture decisions documented in spec documents provided in Dropbox.

Last updated: March 28, 2026

---

## ARMS DEPLOYMENT QUEUE — CURRENT STATE (March 31, 2026)

The deployment queue is managed by ARES. All positions below have passed SENTINEL gates
and are approved for initiation pending regime clearance. The queue fires automatically
when the composite score holds at or below the trigger threshold for three consecutive
5-minute RPE cycles. No PM confirmation required for Tier 0 queue execution.

Architecture AB is an open book — positions are added as they qualify through SENTINEL.
The current 12-position equity book is not a hard cap. FEM and MICS dynamically manage
concentration and weighting as new positions enter.

### NEUTRAL TRIGGER QUEUE — Score ≤ 0.65 (three consecutive cycles)

| # | Ticker | Target Wt. | Entry instruction | Notes |
|---|--------|-----------|-------------------|-------|
| 1 | GOOGL | 4.5–5.0% | 3.5% at NEUTRAL trigger via VWAP. Complete to 5.0% post April 28 earnings confirmation (any positive earnings result). | TWO-LEG CONDITIONAL: Leg 1 = regime-triggered. Leg 2 = EVENT-triggered off April 28 earnings date. Not time-triggered. See Decision Engine spec below. |
| 2 | GEV | 2.5–3.0% | 60% first tranche at trigger via VWAP. 40% second tranche on price flush to $820–840. | TWO-LEG CONDITIONAL: Leg 1 = regime-triggered. Leg 2 = PRICE-triggered at $820–840 level. Different pattern from GOOGL — price trigger, not event trigger. |
| 3 | CEG | 2.0–2.5% | Full size at trigger. VWAP. | Single-leg. Standard regime-triggered entry. |
| 4 | VST | 1.5–2.0% | Full size at trigger. VWAP. | Single-leg. Standard regime-triggered entry. |
| 5 | VRT | +0.7% size-up | Size-up from 2.3% → 3.0%. Limit add at trigger. | Existing position add — not a new initiation. |

### RISK_ON TRIGGER QUEUE — Score ≤ 0.45 (three consecutive cycles)

| # | Ticker | Target Wt. | Entry instruction | Notes |
|---|--------|-----------|-------------------|-------|
| 6 | BE | 1.0–1.5% | Full size at trigger. VWAP. Outright equity position. | Standard single-leg entry. No options. No call sizing. Outright shares only. |
| 7 | NVDA | +1.2% eval | Assess size-up 7.8% → 9.0% if still in correction at RISK_ON. | Evaluation at trigger — not automatic. PM reviews NVDA correction status at RISK_ON before executing. |

### Current Book — Positions Confirmed Unchanged

TSLA 8.8% · NVDA 7.8% · PLTR 5.7% · AMD 7.2% · ANET 4.3% · AVGO 3.7% ·
MU 4.5% (TDC WATCH — thesis review pending) · MRVL 3.5% · ARM 2.5% ·
ETN 2.0% · VRT 2.3% (pre-add) · ALAB 3.42% (post-trim March 27)

---

## DECISION ENGINE — CONDITIONAL TRANCHE LOGIC SPECIFICATION

Josh must build two distinct conditional tranche patterns into the Decision Engine
(src/engine/master_engine.py or a dedicated src/engine/decision_engine.py module).
These are the first examples of multi-leg queue entries in ARMS.

### Pattern A — Event-Triggered Second Tranche (GOOGL)

```python
@dataclass
class QueueEntry:
    ticker: str
    leg: int                    # 1 or 2
    target_weight: float
    trigger_type: str           # 'REGIME' | 'EVENT' | 'PRICE'
    trigger_condition: str      # human-readable description
    # For EVENT triggers:
    event_date: Optional[str]   # ISO date — April 28, 2026 for GOOGL
    event_condition: str        # 'ANY_POSITIVE_EARNINGS'
    execution_method: str       # 'VWAP' | 'LIMIT' | 'MARKET'

# GOOGL example:
# Leg 1: trigger_type='REGIME', threshold=0.65, target=0.035, method='VWAP'
# Leg 2: trigger_type='EVENT', event_date='2026-04-28',
#         event_condition='ANY_POSITIVE_EARNINGS', target=0.015, method='VWAP'
# Leg 2 fires ONLY if Leg 1 has already executed AND earnings are positive.
# Leg 2 does NOT fire if Leg 1 has not yet executed (regime gate still open).
```

### Pattern B — Price-Triggered Second Tranche (GEV)

```python
# GEV example:
# Leg 1: trigger_type='REGIME', threshold=0.65, size=0.60 of target, method='VWAP'
# Leg 2: trigger_type='PRICE', price_level=830, direction='AT_OR_BELOW',
#         size=0.40 of target, method='LIMIT', price=830
# Leg 2 fires ONLY if Leg 1 has already executed AND price touches $820–840.
# Price trigger window: open indefinitely after Leg 1 executes.
# If price never flushes to $820–840: Leg 2 never fires. Position stays at 60%.
```

### Key design rules for conditional tranches:
- Leg 2 NEVER fires before Leg 1 executes. Gate dependency is absolute.
- Leg 1 firing does not guarantee Leg 2. Each leg has its own independent trigger.
- Both legs log to session_log with triggering_module='ARES', leg number, and condition met.
- NVDA size-up (#7) is an EVALUATION at RISK_ON — not automatic. PM reviews at trigger.
  System surfaces it as a Tier 1 item, not a Tier 0 execution.
- BE is outright equity only. No options sizing. No call structures. Outright shares via VWAP.
