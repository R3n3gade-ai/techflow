
# ACHELION ARMS - Historical Backtest Tearsheet (Phase 2)
**Period:** 2022-01-01 to 2022-12-31
**Initial Capital:** $50,000,000.00
**Final NAV:** $40,302,037.58

## 1. Performance Summary
| Metric | ARMS Strategy | S&P 500 (SPY) | Nasdaq 100 (QQQ) |
| :--- | :---: | :---: | :---: |
| **Cumulative Return** | -19.40% | -18.65% | -33.22% |
| **Max Drawdown** | -21.02% | -24.50% | -34.83% |
| **Annualized Volatility**| 10.98% | 20.15% | 26.72% |
| **Sharpe Ratio** | -1.49 | N/A | N/A |

## 2. Risk Engine Diagnostics (L2 & L3)
**Regime Time Allocation:**
- WATCH: 64.8%
- RISK_ON: 35.2%

**Portfolio Drawdown Sentinel (PDS):**
- Days Active (Overrides Fired): 239 days

**Permanent Tail Risk Hedge (PTRH):**
- Average Daily Payout Value: $957,947.38
- Maximum Payout Reached: $4,879,641.26
- Simulated Mechanism: Black-Scholes (-0.35 Delta, 60-90 DTE Rolling)
