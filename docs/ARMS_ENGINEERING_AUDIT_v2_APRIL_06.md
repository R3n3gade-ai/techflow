> **? STALE DOCUMENT — NOT AUTHORITATIVE**
> This document predates significant code changes (April 2026 remediation cycle).
> For current system truth, see: ARMS_NEXT_WAVE_COLD_TRUTH_AUDIT_2026-04-10.md
> and ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md

# ARMS Engineering Audit v2

**Date:** 2026-04-06 (Post-Sprint 3)
**Author:** OpenClaw Engineering
**Project:** Achelion ARMS
**Status:** Internal / GP / Engineering

## Executive Summary
Following the execution of Hardening Sprints 1, 2, and 3, ARMS has matured from a simulated concept into a connected, persistent, and mathematically precise execution framework. The Control Plane is now durable, the IBKR paper broker is live, and Addendum 6 (Delta-Primary Strike Selection) is partially integrated. 

However, a structural audit of the codebase against the FSD v1.1 and THB v4.0 reveals a massive architectural gap: **The v3.1 Legacy Core is missing.** The system is operating on a highly advanced "nervous system" (PTRH, ARES, CDF, DSHP, TDC) but lacks a functioning "brain stem" (ARAS, Macro Compass, Master Engine).

---

## 1. What is Fully Built and Operational (Institution-Grade)

### 1.1 The Execution Control Plane
- **Canonical Execution Contract:** A single, typed `OrderRequest` schema governs all trade generation.
- **Persistent Confirmation Queue:** Tier 1 / Tier 2 approvals survive process reboots and are stored durably with strict timeout enforcement.
- **Correlation Audit:** Every trade request generates a UUID that links the mathematical trigger, queue state, PM approval, and broker submission together in the `SessionLog`.

### 1.2 The Broker Interface
- **IBKR Adapter:** `ib_insync` is successfully wired via an SSH tunnel to the VPS host.
- **Live Ingestion:** ARMS accurately reads Live NAV and active positions from the broker to dynamically calculate coverage drift.

### 1.3 Hedge Management (PTRH & CAM)
- **Addendum 6 Phase 1:** Implemented the Delta-Primary Architecture. ARMS requests the QQQ options chain, filters for 60-90 DTE, evaluates live Delta via `reqTickers`, and mathematically selects the optimal contract closest to `-0.35`.
- **Drift Correction:** Drift logic successfully evaluates the actual options position against the target NAV percentage and generates perfectly sized limit orders.

---

## 2. The Missing Legacy Core (CRITICAL RISK)

The Master Build Document (FSD v1.1) and Technical Handoff Brief (THB v4.0) specify that ARMS is a 7-layer architecture. However, the files designated as "unchanged from v4.0" do not exist in the repository.

### Missing Core Modules:
- `src/engine/aras.py` (The ARAS Composite Risk Assessor)
- `src/engine/macro_compass.py` (The L2 Macro Regime scoring engine)
- `src/engine/master_engine.py` (The L4 Portfolio Construction logic that handles MICS weighting)
- `src/engine/kevlar.py` (Hard limit concentration enforcement)
- `src/engine/slof.py` (Synthetic Leverage Overlay Facility)
- `src/engine/drawdown_sentinel.py` (PDS - Portfolio Drawdown Sentinel)
- `src/engine/factor_exposure.py` (FEM - Factor Exposure Monitor)

**Impact:** `main.py` is currently hardcoding `current_regime="WATCH"` and `regime_score=0.35` because it has no ARAS or Macro Compass to call. The system cannot actually calculate portfolio drift or ceiling exposure limits without these modules.

---

## 3. What is Partially Built / Simulated (Requires Completion)

### 3.1 Intelligence & TDC / Systematic Scan
- `ClaudeWrapper` is returning static mocked JSON responses for specific tickers. It is not currently connected to the Anthropic API.
- `TDC` triggers correctly off the CDM, but the AI reasoning is simulated.

### 3.2 Data Ingestion Pipeline
- `fred_plugin.py`, `pmi_plugin.py`, and `crypto_plugin.py` exist but lack API keys, error handling for stale data, and database caching.

### 3.3 Addendum 6: PTRH Phase 2
- The Delta-Primary selection logic works (Gate 1), but the full Fallback Hierarchy (Gate 2 to Gate 4) is not yet built to expand spread limits or DTE limits dynamically if the options chain is dry.
- The 30-day Drift Calibration baseline database does not exist yet.

### 3.4 Session Log Analytics (SLA) & CCM
- `session_log_analytics.py` currently returns zeros for `cdf_accuracy_rate` and `regime_transition_lag_days` because the query engine to parse historical `SessionLogEntry` JSON lines is not built.
- `conviction_calibration.py` lacks the mathematical correlation engine to optimize MICS weights.

---

## 4. Immediate Engineering Roadmap (Sprint 4 & 5)

### Sprint 4: Rebuilding the Core (The Brain Stem)
1. Reconstruct `macro_compass.py` to ingest the data pipeline and score the regime.
2. Reconstruct `aras.py` to calculate the 15%, 40%, 60%, 80%, 100% equity ceilings based on the Macro Compass and RPE advisory signals.
3. Reconstruct `master_engine.py` to dynamically apply MICS conviction levels to position sizing.
4. Reconstruct `drawdown_sentinel.py` (PDS) to enforce the -12% / -18% HWM limit overrides.

### Sprint 5: The Daily Monitor Presentation Layer
- Convert the raw payload currently printed at the end of `main.py` into the institutional PDF-grade Markdown representation designed in `daily_monitor_renderer.py`.
- Connect the Anthropic API for live TDC AI analysis.
