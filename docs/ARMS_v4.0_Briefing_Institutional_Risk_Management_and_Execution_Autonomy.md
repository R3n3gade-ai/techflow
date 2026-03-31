# ARMS v4.0 Briefing: Institutional Risk Management and Execution Autonomy

## Executive Summary
The **Achelion Risk Management System (ARMS) v4.0** represents the transition from human-managed risk to a fully autonomous decision and execution architecture. The system operates on the **Architecture AB (58/20/14/8)** framework, distributing capital across Equity, AI Infrastructure, Defensive Sleeve, and Cash/Hedge reserves.

Key upgrades in v4.0 include:
*   **PDS (Portfolio Drawdown Sentinel):** An independent, high-latency backstop protecting NAV against model failure.
*   **CAM (Coverage Adequacy Model):** Autonomous management of the Permanent Tail Risk Hedge (PTRH).
*   **MICS (Model-Implied Conviction Score):** Data-driven position sizing that removes subjective conviction assignment.
*   **Anticipatory Intelligence Layer:** Identifying market shifts 2 to 4 quarters ahead of consensus using linguistic velocity and alternative data.

---

## 1. Authority Hierarchy and Regime Management
The ARMS architecture is governed by a strict hierarchy. **"Silence is trust in the architecture."** No human intervention can increase risk; overrides are permitted only to move the portfolio toward a more defensive posture.

### 1.1 Decision Authority Hierarchy
| Authority | Function | Override Rule |
| :--- | :--- | :--- |
| **ARAS** | Absolute regime ceiling provider. | No human override. |
| **PDS** | Drawdown ceiling backstop (-12% / -18%). | Lower of ARAS or PDS always prevails. |
| **FEM** | Advisory factor concentration monitor. | Advisory only; triggers hedge multipliers. |
| **PTRH** | Permanent Tail Risk Hedge (QQQ Puts). | Tier 0 sizing; PM can only suspend with GP approval. |
| **PM + GPs** | Human oversight and thesis seeding. | May override ceilings to be MORE defensive only. |

### 1.2 Regime-Based Exposure Ceilings (ARAS)
The Achelion Risk Assessment System (ARAS) calculates a composite regime score (0.0 to 1.0) every five minutes.
*   **RISK_ON (0.00–0.30):** 100% Equity Ceiling. SLOF active.
*   **WATCH (0.31–0.50):** 100% Equity Ceiling. SLOF active.
*   **NEUTRAL (0.51–0.65):** 75% Equity Ceiling. SLOF reduced.
*   **DEFENSIVE (0.66–0.80):** 40% Equity Ceiling. SLOF removed.
*   **CRASH (>0.80):** 15% Equity Ceiling. SLOF removed; ARES re-entry gates locked.

---

## 2. Core Risk Management Modules

### 2.1 Portfolio Drawdown Sentinel (PDS)
PDS protects Net Asset Value (NAV) against the High-Water Mark (HWM) independently of regime calls.
*   **WARNING (-8%):** Advisory alert for heightened monitoring.
*   **DELEVERAGE 1 (-12%):** Tier 0 enforcement of a **60% gross ceiling**.
*   **DELEVERAGE 2 (-18%):** Tier 0 enforcement of a **30% gross ceiling**; triggers LP disclosure.

### 2.2 Factor Exposure Monitor (FEM)
FEM identifies hidden correlations (e.g., AI Capex, Taiwan manufacturing, Dollar sensitivity).
*   **WATCH (>65%):** Documentation required; intentional vs. accidental check.
*   **ALERT (>80%):** Mandatory review within 24 hours. Triggers a **1.30x Concentration Multiplier** in the CAM hedging model. PM must reaffirm conviction or trim.

### 2.3 Conviction Decay Function (CDF)
CDF prevents "thesis drift" by decaying weights of positions underperforming QQQ by >10pp.
*   **Day 45:** 0.80x weight multiplier (Tier 0).
*   **Day 90:** 0.60x weight multiplier (Tier 0).
*   **Day 135:** Mandatory fundamental review; default to orderly exit (Tier 1).

---

## 3. Tail Risk and Defensive Sleeve Protocols

### 3.1 Coverage Adequacy Model (CAM)
CAM governs the **PTRH**, recalculating required QQQ ATM put coverage every five minutes using dynamic multipliers:
*   **Regime Multiplier:** 1.0x (Risk_On) | 1.25x (Neutral) | 1.5x (Defensive) | 2.0x (Crash).
*   **Exposure Multiplier:** Scales from 0.67x (zero exposure) to 1.0x (full exposure).
*   **Concentration Multiplier:** 1.0x (Normal) to 1.30x (FEM Alert).
*   **Acute Stress Multiplier:** Based on Macro Stress Score (Brent, 10Y, VIX, Spreads). Capped at 1.60x.
*   **Safeguards:** Hedge Floor of **2.4% NAV** (Crash); Hedge Ceiling capped at **3.5% NAV** to limit drag.

### 3.2 Defensive Sleeve Harvest Protocol (DSHP)
DSHP crystallizes gains in the 14% defensive architecture (Gold/SGOL, Managed Futures/DBMF).
*   **SGOL:** Trim to 2% target if appreciation >20%.
*   **DBMF:** Trim to 5% target if appreciation >15% or weight drift >1.5pp.
*   **Execution:** Proceeds redeposited into SGOV (within the sleeve), maintaining the 14% architecture.

---

## 4. Anticipatory Intelligence and MICS
The Intelligence Layer identifies signals before they reach consensus, feeding the **Model-Implied Conviction Score (MICS)**.

| Module | Data Source | Lead Time | Target Focus |
| :--- | :--- | :--- | :--- |
| **ELVT** (Earnings Language) | SEC EDGAR/8-K Transcripts | 2–3 Quarters | Linguistic Velocity / Guidance |
| **JPVI** (Job Posting Velocity) | Adzuna / LinkedIn | 4–12 Months | Capex Leading Indicators |
| **PFVT** (Patent Filing Velocity) | USPTO PatentsView | 12–36 Months | IP / Tech Advantage |
| **SCCR** (Supply Chain X-Ref) | Manifests / Satellite Data | 2–4 Quarters | Hardware / Logistics |

**MICS Scoring:** Position sizing is derived from a 0–10 score based on SENTINEL gate data and the **Source Taxonomy** (Cat A: Primary, Cat B: Pattern, Cat C: Synthesis). PMs may override MICS by ±1 level with documentation.

---

## 5. Infrastructure and Execution Autonomy

### 5.1 The Fortress (AWS Architecture)
All logic resides in a high-availability cloud environment to ensure <30-second latency for circuit breakers.
*   **Compute:** AWS ECS (Fargate) for async backend logic (Python 3.11/FastAPI).
*   **Cache:** Redis (ElastiCache) for real-time SYS-1 circuit breakers and correlation monitoring.
*   **Storage:** PostgreSQL (RDS) for the immutable audit trail and state management.

### 5.2 Execution Tiers
*   **Tier 0 (Fully Autonomous):** Immediate execution (ARAS Ceilings, PDS, CDF, PTRH). No PM veto.
*   **Tier 1 (Default Execute):** System queues action (DSHP, PERM, SENTINEL entry) with a **4-hour veto window**.
*   **Tier 2 (PM Confirmation):** Requires explicit PM response and GP co-sign (MICS ±2 overrides, structural architecture changes).

### 5.3 Liquidity-Adjusted Execution Priority (LAEP)
In CRISIS mode (VIX >45), execution priority is reversed to exit illiquid positions first:
1. **BSOL (Solana)** | 2. **ETHB (Ethereum)** | 3. **IBIT (Bitcoin)** | 4. **Equities (NVDA/TSLA)**.
