> **? STALE DOCUMENT — NOT AUTHORITATIVE**
> This document predates significant code changes (April 2026 remediation cycle).
> For current system truth, see: ARMS_NEXT_WAVE_COLD_TRUTH_AUDIT_2026-04-10.md
> and ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md

# The Codebase Game Plan (Order of Execution) v2.0

## Strategy: Risk Elimination & Value Creation
We are building ARMS by prioritizing **Risk Elimination** and **Value Creation**, strictly adhering to **FSD v1.1** and the **Reconciliation Guidelines**. This sequence ensures the system's "brain" is functional before we connect the "muscles" to the market.

---

### Step 1: Foundation & Plumbing (P0 - COMPLETED)
The legacy foundation (68/25/7) has been decommissioned. The system now operates on the Architecture AB framework.
- **Environment:** Postgres, Redis, and Python 3.11+ VENV established.
- **Allocation Fix:** `src/engine/mics.py` and configuration layers updated to **Architecture AB (58/20/14/8)** conviction-squared weights.
- **Defense Sleeve:** TLT, SGOL, and DBMF integrated into the mapping; hardcoded exemption from ARAS deleveraging protocols verified.
- **Kevlar Limits:** Hard limits enforced (22% max single position, 3% minimum, 48% total AI sector cap).
- **ARAS Logic:** `aras.py` (legacy) logic migrated to `src/engine/` with **CORRELATED** stress source detection.

### Step 2: Intelligence Frontiers (Phase 1 - ACTIVE)
Closing the five "Immediate-Build Frontiers" to unlock Tier 0 autonomy.
- **MICS (Model-Implied Conviction Score):** **[DONE]** `src/engine/mics.py`. Fully formulaic sizing based on 5-gate SENTINEL output.
- **Feed-Agnostic Pipeline:** **[IN PROGRESS]** `src/data_feeds/`. Core interface and FRED plugin complete. Binance and S&P Global plugins pending.
- **PMI Nowcast Engine:** **[PLANNED]** Implementation of PMI Module Spec v1.0. Transitioning from ISM to S&P Global US Mfg PMI with dual-layer live/nowcast blending.
- **Confirmation Queue:** **[DONE]** `src/execution/confirmation_queue.py`. 3-option response logic (Execute, Hold/Inform, Veto) for Tier 1 actions.
- **Audit Log (SLA):** **[DONE]** `src/reporting/audit_log.py`. Immutable structured logging to fuel the Phase 2 learning loop.

### Step 3: Behavioral Correctness (Phase 2 - RULES)
Teaching ARMS the "Rules of Engagement" and capital preservation.
- **Cash/Hedge Budgets:** Implementation of the tiered 8% structure (1.2% core hedge, 3.8% buffer, 2.0% regime reserve).
- **Execution Protocol:** Hardcoded deleveraging sequence:
    1. **SLOF** (Short-Term Liquidity)
    2. **High Beta Equity**
    3. **Crypto**
    4. **Pro-rata Equity**
    5. **Defense Sleeve** (Exempt)
- **Hedge Architecture v5.2:** Implementation of **QQQ Outright Puts** logic. All legacy bear-spread code purged from the engine.
- **PTRH Automation:** CAM (Coverage Adequacy Model) integration for autonomous roll and sizing.

### Step 4: Execution Systems (Phase 2 - MUSCLES)
Connecting the autonomous brain to market liquidity.
- **SYS-1 (Circuit Breakers):** Async WebSocket listeners for QQQ, VIX, and IBIT to trigger intraday overrides.
- **SYS-5 (Correlation Monitor):** Rolling 1-hour equity/crypto correlation monitoring via Redis.
- **SYS-3 & SYS-6:** Implementation of pre-calculated order states and +2 day drawdown escalation logic.
- **IBKR Integration:** **[ACTIVE]** `src/execution/broker_api.py`. Transitioning to `ib_insync` for live paper trading validation.

### Step 5: Resilience & Expansion (Phase 3 - SCALE)
Bulletproofing the fund for institutional-grade autonomy.
- **ARES (Re-Entry System):** 3-gate re-entry logic (Stress Normalization, Macro Confirmation, Sentiment Capitulation) with staged tranche rollouts.
- **MC-RSS:** Integration of Retail Sentiment Score as the contrarian override to the Macro Compass.
- **Incapacitation Protocol:** Strict fallback timers (4h, 24h, 72h) that default the portfolio to NEUTRAL or DEFENSIVE if PM signal is lost.
- **Systematic Scan Engine:** **[ACTIVE]** Integration of Claude 3.5/4.0 to process SEC EDGAR filings for the Monday intelligence briefs.
