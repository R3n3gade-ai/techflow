
# ACHELION ARMS - Historical Backtest Tearsheet (Phase 2)
**Period:** 2020-01-01 to 2022-12-31
**Initial Capital:** $50,000,000.00
**Final NAV:** $73,700,000.00

## 1. Performance Summary
| Metric | ARMS Strategy | S&P 500 (SPY) | Nasdaq 100 (QQQ) |
| :--- | :---: | :---: | :---: |
| **Cumulative Return** | 47.40% | 24.80% | 25.40% |
| **Max Drawdown** | -19.62% | -33.72% | -35.12% |
| **Annualized Volatility**| 13.45% | 20.77% | 24.66% |
| **Sharpe Ratio** | 0.78 | N/A | N/A |

## 2. Risk Engine Diagnostics (L2 & L3)
**Regime Time Allocation:**
- RISK_ON: 52.8%
- WATCH: 39.5%
- NEUTRAL: 4.5%
- DEFENSIVE: 3.3%

**Portfolio Drawdown Sentinel (PDS):**
- Days Active (Overrides Fired): 371 days

**Permanent Tail Risk Hedge (PTRH):**
- Average Daily Payout Value: $1,231,587.35
- Maximum Payout Reached: $8,225,884.43
- Simulated Mechanism: Black-Scholes (-0.35 Delta, 60-90 DTE Rolling)
