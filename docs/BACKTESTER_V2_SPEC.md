# ARMS Customizable Backtesting Engine (v2.0)
**Architecture Specification for Client Deployment**

## 1. Executive Summary
The current Phase 2 Backtester runs a hardcoded Architecture AB portfolio (58/20/14/8) and assumes cash deployment on Day 1. To support commercial licensing and LP/Client due diligence, the engine must evolve into a fully customizable sandbox. 

Clients must be able to input their exact historical portfolio (tickers, entry prices, quantities, and cash balance) on a specific start date, and run the complete 7-Layer ARMS architecture forward to any end date to see exactly how the system would have protected or governed their specific capital.

## 2. Full Architecture & Pillar Integration Flow
Every single live module from L2 to L5 must be sequentially wired into the Backtester's daily evaluation loop.

### 2.1 The Input Layer (`portfolio_config.json`)
Instead of hardcoding weights, the engine will ingest a user-defined JSON configuration file containing:
*   `start_date` / `end_date`
*   `initial_cash`
*   `positions`: List of objects containing `ticker`, `quantity`, and `entry_price`.
*   `mics_overrides`: Optional static Conviction Scores for their tickers.

### 2.2 The Daily Evaluation Loop (All 7 Pillars Active)
The engine steps through time, applying **all** live ARMS modules to the custom book in exact operational order:

1.  **L2 Brain (The Navigator):** `macro_compass.py` calculates the exact regime (RISK_ON ... CRASH) based on the daily VIX, 10Y, HY Spreads, and PMI. `aras.py` translates this into the canonical equity ceiling.
2.  **L3 PDS (Drawdown Sentinel):** `drawdown_sentinel.py` monitors the custom NAV against its High-Water Mark for the -12% / -18% hard-stop overrides, regardless of what ARAS says.
3.  **L3 FEM (Factor Exposure Monitor):** `factor_exposure.py` scans the custom book. If AI infrastructure exposure exceeds 65% (Watch) or 80% (Alert), it flags the concentration risk.
4.  **L3 CDF (Conviction Decay Function):** `cdf.py` tracks every individual ticker in the user's book against QQQ. If a stock underperforms by 10 percentage points for 45/90/135 days, the engine automatically mathematically decays its weight multiplier (0.80x, 0.60x), forcing the Master Engine to trim the position.
5.  **L3 DSHP (Defensive Sleeve Harvest Protocol):** `dshp.py` monitors the user's Gold (SGOL) and Managed Futures (DBMF). If gold spikes >20% during the backtest, it automatically queues a Tier 1 order to trim the gains back to target weight.
6.  **L3 PTRH (Permanent Tail Risk Hedge) & CAM:** `cam.py` calculates the required QQQ Put notional based on the user's *exact* daily equity exposure, VIX, and FEM score. The engine mathematically "purchases" the required -0.35 Delta contracts using the Black-Scholes proxy.
7.  **L3 SLOF & PERM (Upside & Yield Harvesting):** `slof.py` activates synthetic 1.25x leverage for top-conviction names if the regime is RISK_ON/WATCH. `perm.py` sells covered calls against decaying (CDF < 0.80x) positions to harvest yield.
8.  **L4 Master Engine:** Evaluates the MICS scores, CDF decay multipliers, ARAS/PDS ceilings, and `kevlar.py` (22% hard single-name cap) to generate the final ideal target weights for the custom book.
9.  **L5 LAEP (Liquidity-Adjusted Execution Protocol):** Translates the Master Engine's delta orders into VWAP tranches based on that day's closing VIX (e.g., 30-min vs 90-min windows).

### 2.3 The Output Layer: Institutional Tear Sheet & Audit Trail
At the end of the simulation, the engine generates two artifacts:
1.  **The Performance Tear Sheet (Markdown/PDF):**
    *   Custom Portfolio Return vs. S&P 500 (SPY).
    *   Max Drawdown comparison.
    *   Annualized Volatility & Sharpe.
2.  **The Action Ledger (CSV/JSON):**
    *   A chronological log of every autonomous move ARMS made.
    *   *Example:* `2020-03-09: VIX crossed 45. Regime -> CRASH. PDS fired at -12%. Sold 4,500 shares of AAPL. Purchased $120,000 notional QQQ Puts. LAEP mode: CRISIS.`
