import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np

def generate_tearsheet(history: pd.DataFrame, start_date: str, end_date: str, initial_capital: float):
    # Benchmark Returns (assuming we buy and hold SPY and QQQ from Day 1)
    first_spy = history['SPY_Price'].iloc[0]
    last_spy = history['SPY_Price'].iloc[-1]
    spy_return = (last_spy / first_spy) - 1
    
    first_qqq = history['QQQ_Price'].iloc[0]
    last_qqq = history['QQQ_Price'].iloc[-1]
    qqq_return = (last_qqq / first_qqq) - 1
    
    # Strategy Returns
    final_nav = history['NAV'].iloc[-1]
    strat_return = (final_nav / initial_capital) - 1
    
    # Daily Returns
    history['Daily_Return'] = history['NAV'].pct_change()
    history['SPY_Daily'] = history['SPY_Price'].pct_change()
    history['QQQ_Daily'] = history['QQQ_Price'].pct_change()
    
    # Volatility (Annualized)
    trading_days = 252
    strat_vol = history['Daily_Return'].std() * np.sqrt(trading_days)
    spy_vol = history['SPY_Daily'].std() * np.sqrt(trading_days)
    qqq_vol = history['QQQ_Daily'].std() * np.sqrt(trading_days)
    
    # Sharpe Ratio (Assuming 2% Risk-Free Rate)
    rf_rate = 0.02
    daily_rf = rf_rate / trading_days
    strat_sharpe = (history['Daily_Return'].mean() - daily_rf) / history['Daily_Return'].std() * np.sqrt(trading_days)
    
    # Max Drawdown
    cumulative_max = history['NAV'].cummax()
    drawdown = (history['NAV'] / cumulative_max) - 1
    max_drawdown = drawdown.min()
    
    spy_cummax = history['SPY_Price'].cummax()
    spy_dd = (history['SPY_Price'] / spy_cummax) - 1
    spy_max_dd = spy_dd.min()
    
    qqq_cummax = history['QQQ_Price'].cummax()
    qqq_dd = (history['QQQ_Price'] / qqq_cummax) - 1
    qqq_max_dd = qqq_dd.min()
    
    # Regime States Breakdown
    regime_counts = history['Regime'].value_counts(normalize=True)
    
    # PDS Activations
    pds_active_days = (history['PDS_Ceiling'] < 1.0).sum()
    
    report = f"""
# ACHELION ARMS - Historical Backtest Tearsheet
**Period:** {start_date} to {end_date}
**Initial Capital:** ${initial_capital:,.2f}
**Final NAV:** ${final_nav:,.2f}

## 1. Performance Summary
| Metric | ARMS Strategy | S&P 500 (SPY) | Nasdaq 100 (QQQ) |
| :--- | :---: | :---: | :---: |
| **Cumulative Return** | {strat_return:.2%} | {spy_return:.2%} | {qqq_return:.2%} |
| **Max Drawdown** | {max_drawdown:.2%} | {spy_max_dd:.2%} | {qqq_max_dd:.2%} |
| **Annualized Volatility**| {strat_vol:.2%} | {spy_vol:.2%} | {qqq_vol:.2%} |
| **Sharpe Ratio** | {strat_sharpe:.2f} | N/A | N/A |

## 2. Risk Engine Diagnostics (L2 & L3)
**Regime Time Allocation:**
"""
    for regime, pct in regime_counts.items():
        report += f"- {regime}: {pct:.1%}\n"
        
    report += f"\n**Portfolio Drawdown Sentinel (PDS):**\n"
    report += f"- Days Active (Overrides Fired): {pds_active_days} days\n"
    
    # Save the report
    with open('/data/.openclaw/workspace/achelion_arms/SAMPLES/backtest_tearsheet_2020.md', 'w') as f:
        f.write(report)
        
    print(report)

if __name__ == "__main__":
    from simulation.historical_engine import run_simulation
    res = run_simulation("2020-01-01", "2020-12-31")
    generate_tearsheet(res.history, "2020-01-01", "2020-12-31", 50000000.0)
