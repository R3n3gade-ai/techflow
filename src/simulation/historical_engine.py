import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from typing import List, Dict

from data_feeds.interfaces import SignalRecord
from engine.macro_compass import calculate_macro_regime_score
from engine.aras import calculate_aras_ceiling
from engine.drawdown_sentinel import run_pds_check
from simulation.data_loader import load_historical_data
from datetime import datetime, timezone

class BacktestResult:
    def __init__(self, history: pd.DataFrame):
        self.history = history

def run_simulation(start_date: str, end_date: str, initial_capital: float = 50_000_000.0) -> BacktestResult:
    df = load_historical_data(start_date, end_date)
    
    # State tracking
    nav = initial_capital
    hwm = initial_capital
    
    # Simple Phase 1 Portfolio: 100% QQQ initially (Cash/Equity mix)
    # We will track the number of QQQ shares and Cash balance.
    # At start, we buy QQQ up to the ARAS ceiling.
    shares_qqq = 0.0
    cash = initial_capital
    
    history_records = []
    
    for date, row in df.iterrows():
        # 1. Mark to Market (Beginning of Day)
        qqq_price = row['QQQ_CLOSE']
        spy_price = row['SPY_CLOSE']
        
        current_equity_value = shares_qqq * qqq_price
        nav = cash + current_equity_value
        
        if nav > hwm:
            hwm = nav
            
        # 2. Build Signals for Macro Compass
        iso_date = date.replace(tzinfo=timezone.utc).isoformat()
        signals = [
            SignalRecord(ticker='MACRO', signal_type='VIX_INDEX', value=row['VIX'], raw_value=row['VIX'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE'),
            SignalRecord(ticker='MACRO', signal_type='HY_CREDIT_SPREAD', value=row['HY_SPREAD'], raw_value=row['HY_SPREAD'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE'),
            SignalRecord(ticker='MACRO', signal_type='PMI_NOWCAST', value=row['PMI'], raw_value=row['PMI'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE'),
            SignalRecord(ticker='MACRO', signal_type='10Y_TREASURY_YIELD', value=row['10Y_YIELD'], raw_value=row['10Y_YIELD'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE')
        ]
        
        # 3. L2 Brain Assessment
        regime_score = calculate_macro_regime_score(signals)
        aras_out = calculate_aras_ceiling(regime_score)
        
        # 4. L3 Safety Overrides (PDS)
        pds_out = run_pds_check(nav, hwm)
        
        # 5. Master Engine Target
        # The ultimate equity ceiling is the minimum of ARAS and PDS
        target_equity_pct = min(aras_out.equity_ceiling_pct, pds_out.pds_ceiling)
        
        # 6. Rebalance Portfolio (End of Day / Action)
        target_equity_value = nav * target_equity_pct
        
        # Calculate delta
        delta_value = target_equity_value - current_equity_value
        
        # Execute Trade
        if abs(delta_value) > 1.0: # Minor threshold to avoid float precision trades
            shares_to_trade = delta_value / qqq_price
            shares_qqq += shares_to_trade
            cash -= delta_value # Ignoring slippage/commissions for Phase 1
            
            current_equity_value = shares_qqq * qqq_price
            nav = cash + current_equity_value
            
        # 7. Record State
        history_records.append({
            'Date': date,
            'NAV': nav,
            'QQQ_Price': qqq_price,
            'SPY_Price': spy_price,
            'VIX': row['VIX'],
            'HY_Spread': row['HY_SPREAD'],
            'Regime': aras_out.regime,
            'Regime_Score': regime_score,
            'Equity_Ceiling': aras_out.equity_ceiling_pct,
            'PDS_Status': pds_out.status,
            'PDS_Ceiling': pds_out.pds_ceiling,
            'Target_Equity_Pct': target_equity_pct,
            'Actual_Equity_Pct': current_equity_value / nav,
            'Drawdown': pds_out.drawdown_pct
        })
        
    history_df = pd.DataFrame(history_records)
    history_df.set_index('Date', inplace=True)
    return BacktestResult(history_df)

if __name__ == "__main__":
    res = run_simulation("2020-01-01", "2020-05-01")
    print(res.history[['NAV', 'Regime', 'Equity_Ceiling', 'Drawdown']].tail())
