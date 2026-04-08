# ARMS Historical Simulation & Backtesting Engine
**Architecture Specification v1.0**
**Date:** April 8, 2026

## 1. Executive Summary
The General Partner Briefing states: *"The 2022 backtest shows ARMS at -16.1% in a year when the Nasdaq-100 fell 32.6%. The result: +47.4% over three years versus the S&P 500's +24.8%."*

To cryptographically verify these claims and pressure-test future architecture upgrades, Achelion requires a native, programmatic Historical Simulation Engine. This engine will not rely on static Excel approximations. It will feed historical time-series data directly into the *exact* live ARMS production modules (ARAS, PDS, KEVLAR, LAEP, PTRH) to simulate day-by-step performance.

## 2. Core Objectives
1. **Cryptographic Verification:** Recreate the 2020-2022 full-cycle backtest using the live `src/engine/` Python modules to mathematically prove the defensive architecture functions as claimed.
2. **Stress Testing:** Allow the PM to inject hypothetical or historical shock events (e.g., COVID-19, 2008 GFC, 1987 Black Monday) against the current Architecture AB portfolio (58/20/14/8).
3. **Parameter Optimization:** Provide a sandbox to backtest adjustments to the Macro Compass weightings or PDS thresholds before deploying them to the live fortress.

## 3. Architecture & Data Flow

### 3.1 The "Time Machine" (Data Ingestion Layer)
The engine will bypass the live `broker_api.py` and `fred_plugin.py` connections. Instead, it will pre-fetch and cache historical daily data for the specified date range (e.g., `2020-01-01` to `2022-12-31`).
*   **Macro Signals:** Historical VIX, 10Y Treasury Yield, HY Credit Spreads, and PMI.
*   **Portfolio Pricing:** Daily Adjusted Close prices for all requested equities and defensive sleeve assets (SGOV, SGOL, DBMF).
*   **Options Proxy (PTRH):** Because historical options chain data is prohibitively expensive and complex to query at the `-0.35 Delta` level for every day of a 3-year backtest, the engine will use a mathematical proxy (e.g., the CBOE QQQ Volatility Index or a Black-Scholes estimator) to approximate the daily mark-to-market value of the 60-90 DTE tail hedge.

### 3.2 The Daily Orchestrator (The Step Loop)
The engine will run a `for date in date_range:` loop, simulating the 5:15 AM CT Portfolio Snapshot and 5:20 AM CT Module Sweep.

**Step Sequence per Day:**
1.  **Mark to Market:** Update the NAV based on the previous day's closing prices for all held positions.
2.  **L2 Brain Assessment:** Feed the day's historical macro signals into `macro_compass.py` to calculate the Regime Score (0.0-1.0) and `aras.py` to determine the Equity Ceiling (15%-100%).
3.  **L3 Safety Overrides:** Feed the new NAV and the historical High-Water Mark into `drawdown_sentinel.py`. If the simulated NAV drops -12%, the PDS generates a hard `DELEVERAGE_1` signal.
4.  **L4 Portfolio Construction:** The Master Engine recalculates target weights based on the ARAS ceiling and PDS overrides.
5.  **Rebalancing:** If the regime shifts (e.g., NEUTRAL to DEFENSIVE), the engine mathematically "sells" the required equity exposure into Cash at that day's closing price.
6.  **State Persistence:** Record the day's NAV, Regime, and Equity Exposure to the simulation log.

### 3.3 The Analytics Output (The Tearsheet)
Upon completing the date range loop, the engine will generate an institutional performance report containing:
*   **Cumulative Return:** ARMS Strategy vs. S&P 500 (SPY) vs. Nasdaq-100 (QQQ).
*   **Annualized Volatility & Sharpe Ratio.**
*   **Maximum Drawdown:** The deepest peak-to-trough drop (Proving the PDS/PTRH safety net).
*   **Regime Transition Timeline:** A chronological chart mapping exactly when the system autonomously shifted ceilings (e.g., "Entered CRASH regime on Feb 24, 2020. Exited to WATCH on April 15, 2020").

## 4. Implementation Phasing

### Phase 1: Static Book Simulation
*   **Goal:** Prove the ARAS and PDS modules protect a static portfolio during a known crash.
*   **Mechanics:** Initialize a fixed portfolio (e.g., 100% QQQ) on Jan 1, 2020. Run the daily loop through Dec 31, 2020.
*   **Expected Result:** The system should autonomously detect the VIX spike, shift to CRASH, deleverage the QQQ to 15%, hold cash, and ride out the COVID-19 bottom, drastically outperforming a buy-and-hold QQQ strategy in max drawdown.

### Phase 2: Dynamic Book & Tail Hedge
*   **Goal:** Introduce the PTRH options proxy and the Defensive Sleeve (Gold/Treasuries).
*   **Mechanics:** Run the full Architecture AB target weights. Integrate the Black-Scholes proxy to simulate the QQQ puts expanding in value during the crash.

### Phase 3: AI/TDC Integration (Optional Future Frontier)
*   **Goal:** Backtest the intelligence layer.
*   **Mechanics:** Feed historical news headlines (e.g., from a Bloomberg archive API) into the `cdm.py` and `tdc.py` modules to see if the LLM would have accurately flagged "IMPAIRED" thesis integrity *before* the price fully collapsed.

## 5. Required Dependencies
*   `yfinance` (for historical daily equity and index data).
*   `pandas` & `numpy` (for vectorized performance calculations and tearsheet generation).
*   `matplotlib` or `plotly` (for generating the regime transition timeline charts).
*   `py_vollib` or similar (for Black-Scholes options proxy estimation).
