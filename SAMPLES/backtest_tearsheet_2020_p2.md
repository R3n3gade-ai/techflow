
# ACHELION ARMS - Historical Backtest Tearsheet (Phase 2)
**Period:** 2020-01-01 to 2020-12-31
**Initial Capital:** $50,000,000.00
**Final NAV:** $76,131,979.31

## 1. Performance Summary
| Metric | ARMS Strategy | S&P 500 (SPY) | Nasdaq 100 (QQQ) |
| :--- | :---: | :---: | :---: |
| **Cumulative Return** | 52.26% | 16.64% | 45.61% |
| **Max Drawdown** | -17.22% | -33.72% | -28.56% |
| **Annualized Volatility**| 15.54% | 27.82% | 29.69% |
| **Sharpe Ratio** | 1.82 | N/A | N/A |

## 2. Risk Engine Diagnostics (L2 & L3)
**Regime Time Allocation:**
- WATCH: 50.7%
- RISK_ON: 26.0%
- NEUTRAL: 13.4%
- DEFENSIVE: 9.9%

**Portfolio Drawdown Sentinel (PDS):**
- Days Active (Overrides Fired): 47 days

**Permanent Tail Risk Hedge (PTRH):**
- Average Daily Payout Value: $693,201.77
- Maximum Payout Reached: $3,569,204.79
- Simulated Mechanism: Black-Scholes (-0.35 Delta, 60-90 DTE Rolling)
