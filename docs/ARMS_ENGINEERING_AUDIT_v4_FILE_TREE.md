# ARMS Engineering Audit v4 (File Tree & Execution Pipeline)

**Date:** 2026-04-06
**Status:** Canonical Audit of the Workspace against THB v4.0

This audit verifies the exact physical presence of the 7-Layer execution pipeline mapped in the Technical Handoff Brief v4.0. While Sprints 1-4 successfully built and integrated the new institutional logic (MICS, CAM, PTRH, DSHP, CDM, TDC, RPE, ARES, CDF, CCM, TRP, AUP, PDS, FEM, ARAS, Macro Compass, Master Engine), an audit of the underlying "muscle memory" reveals missing legacy components.

## 1. What is Fully Intact and Operational
- **The Brain Stem (L2/L3/L4):** Rebuilt during Sprint 4. `macro_compass.py`, `aras.py`, `master_engine.py`, `kevlar.py`, `drawdown_sentinel.py`, and `factor_exposure.py` exist and run perfectly in the orchestrator.
- **The New Nervous System (L3 Addenda):** MICS, CAM, PTRH, DSHP, CDM, TDC, RPE, ARES, CDF, CCM, TRP, and AUP are fully coded and mathematically sound.
- **Data Ingestion (L1):** `FRED` and `Crypto` pipelines are securely connected via `.env` endpoints.
- **Execution Endpoint (L6):** `IBKRBroker` adapter correctly pulls positions/NAV over the SSH tunnel.

## 2. What is Missing (The L5 Execution Core & Sub-Modules)
The THB v4.0 explicitly lists a highly robust order processing engine inherited from v3.1. These files are not in the repository:

### 2.1 The `src/execution/` Order Book & Safety Subsystems
- `order_book.py` (The LAEP — Liquidity-Adjusted Execution Protocol. This is supposed to translate the `OrderRequest` into VWAP/Market orders based on VIX thresholds).
- `circuit_breaker.py` (Market panic halts)
- `overnight_monitor.py`
- `correlation_monitor.py`
- `escalation_engine.py` (Escalation Rule v2 - cumulative 2.5% auto-suppress)
- `trade_order_generator.py`
- `pm_protocol.py`

### 2.2 The `src/modules/` Stress Engines (ARAS sub-components)
- `deleveraging_risk.py`
- `crypto_microstructure.py`
- `margin_stress.py`
- `dealer_gamma.py`
- `pcr_regime.py`
- `shutdown_risk.py`
- `stress_scenarios.py` (SSL - Stress Scenario Library. Supposed to run 8 historical crash scenarios against the daily snapshot).

### 2.3 `src/engine/` Leftovers
- `slof.py` (Synthetic Leverage Overlay Facility)
- `perm.py` (PERM Covered Call Execution)

## 3. Operational Reality & Resolution
Right now, `main.py` takes the `OrderRequest` from PTRH and blindly assumes it can be sent directly to `IBKRBroker`. This works on paper, but it physically bypasses **L5 Order Book (LAEP)** which dictates execution window timing (30m, 60m, 90m) and slippage budgets based on liquidity. 

Because we are holding on the AI Layer (Claude Wrapper) until we pick a model, the immediate priority should be:
**Rebuilding `order_book.py` (LAEP)** so that when the system trades, it respects liquidity rules, priority ordering, and circuit breakers.