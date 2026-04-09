import sys
import os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from typing import List, Dict

from data_feeds.interfaces import SignalRecord
from engine.macro_compass import calculate_macro_regime_score
from engine.aras import calculate_aras_ceiling
from engine.drawdown_sentinel import run_pds_check
from engine.cam import calculate_required_notional, CamInputs
from simulation.data_loader_phase2 import load_historical_data_phase2
from datetime import datetime, timezone

def norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def black_scholes_put(S, K, T, r, sigma):
    """
    S: spot price
    K: strike price
    T: time to maturity (in years)
    r: risk-free rate
    sigma: volatility
    """
    if T <= 0:
        return max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

def bs_delta_put(S, K, T, r, sigma):
    if T <= 0:
        return -1.0 if S < K else 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return norm_cdf(d1) - 1.0

def find_strike_for_delta(S, T, r, sigma, target_delta=-0.35):
    # Binary search for strike
    low = S * 0.5
    high = S * 1.5
    for _ in range(30):
        mid = (low + high) / 2
        d = bs_delta_put(S, mid, T, r, sigma)
        if d > target_delta: # e.g. -0.2 > -0.35
            low = mid
        else:
            high = mid
    return (low + high) / 2

class BacktestResult:
    def __init__(self, history: pd.DataFrame):
        self.history = history

def run_simulation_phase2(start_date: str, end_date: str, initial_capital: float = 50_000_000.0) -> BacktestResult:
    df = load_historical_data_phase2(start_date, end_date)
    
    # State tracking
    nav = initial_capital
    hwm = initial_capital
    
    # Portfolio composition
    shares_qqq = 0.0     # Equities (58%)
    shares_btc = 0.0     # Crypto (20%)
    shares_sgov = 0.0    # Cash proxy / short term (8% Cash + 3% SGOV)
    shares_sgol = 0.0    # Gold (2%)
    shares_dbmf = 0.0    # Managed Futures (5%)
    shares_strc = 0.0    # Structured Credit (4%)
    
    # Target allocations
    W_EQ = 0.58
    W_BTC = 0.20
    W_SGOV = 0.03
    W_SGOL = 0.02
    W_DBMF = 0.05
    W_STRC = 0.04
    W_CASH = 0.08
    
    # Initialize allocations
    S_QQQ = df.iloc[0]['QQQ_CLOSE']
    S_BTC = df.iloc[0]['BTC_CLOSE']
    S_SGOV = df.iloc[0]['SGOV_CLOSE']
    S_SGOL = df.iloc[0]['SGOL_CLOSE']
    S_DBMF = df.iloc[0]['DBMF_CLOSE']
    S_STRC = df.iloc[0]['STRC_CLOSE']
    
    shares_qqq = (initial_capital * W_EQ) / S_QQQ
    shares_btc = (initial_capital * W_BTC) / S_BTC
    shares_sgov = (initial_capital * W_SGOV) / S_SGOV
    shares_sgol = (initial_capital * W_SGOL) / S_SGOL
    shares_dbmf = (initial_capital * W_DBMF) / S_DBMF
    shares_strc = (initial_capital * W_STRC) / S_STRC
    cash = initial_capital * W_CASH
    
    # PTRH State
    ptrh_contracts = 0
    ptrh_strike = 0.0
    ptrh_dte = 0
    ptrh_entry_price = 0.0
    
    history_records = []
    
    for i, (date, row) in enumerate(df.iterrows()):
        qqq_price = row['QQQ_CLOSE']
        btc_price = row['BTC_CLOSE']
        sgov_price = row['SGOV_CLOSE']
        sgol_price = row['SGOL_CLOSE']
        dbmf_price = row['DBMF_CLOSE']
        strc_price = row['STRC_CLOSE']
        
        # PTRH Mark to market
        r = row['10Y_YIELD'] / 100.0
        sigma = row['VIX'] / 100.0
        
        # Reduce DTE
        if i > 0 and ptrh_contracts > 0:
            ptrh_dte -= 1
            
        ptrh_value = 0.0
        if ptrh_contracts > 0 and ptrh_dte > 0:
            T = ptrh_dte / 365.0
            opt_price = black_scholes_put(qqq_price, ptrh_strike, T, r, sigma)
            ptrh_value = opt_price * 100 * ptrh_contracts
            
        # 1. Mark to Market
        current_equity_value = shares_qqq * qqq_price
        current_btc_value = shares_btc * btc_price
        current_defensive_value = (shares_sgov * sgov_price) + (shares_sgol * sgol_price) + \
                                  (shares_dbmf * dbmf_price) + (shares_strc * strc_price)
                                  
        nav = cash + current_equity_value + current_btc_value + current_defensive_value + ptrh_value
        
        if nav > hwm:
            hwm = nav
            
        # 2. Macro Compass
        iso_date = date.replace(tzinfo=timezone.utc).isoformat()
        signals = [
            SignalRecord(ticker='MACRO', signal_type='VIX_INDEX', value=row['VIX'], raw_value=row['VIX'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE'),
            SignalRecord(ticker='MACRO', signal_type='HY_CREDIT_SPREAD', value=row['HY_SPREAD'], raw_value=row['HY_SPREAD'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE'),
            SignalRecord(ticker='MACRO', signal_type='PMI_NOWCAST', value=row['PMI'], raw_value=row['PMI'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE'),
            SignalRecord(ticker='MACRO', signal_type='10Y_TREASURY_YIELD', value=row['10Y_YIELD'], raw_value=row['10Y_YIELD'], source='BACKTEST', timestamp=iso_date, cost_tier='FREE')
        ]
        
        regime_score = calculate_macro_regime_score(signals)
        aras_out = calculate_aras_ceiling(regime_score)
        
        # 3. L3 Safety Overrides (PDS)
        pds_out = run_pds_check(nav, hwm)
        
        # Master Engine Target
        target_equity_pct = min(aras_out.equity_ceiling_pct, pds_out.pds_ceiling) * W_EQ
        
        # If CRASH, we might also reduce BTC
        target_btc_pct = W_BTC
        if aras_out.regime == "CRASH":
            target_btc_pct = 0.05
        elif pds_out.pds_ceiling < 1.0:
            target_btc_pct = W_BTC * pds_out.pds_ceiling

        # 4. Rebalance Equities & Crypto
        target_equity_value = nav * target_equity_pct
        delta_eq = target_equity_value - current_equity_value
        if abs(delta_eq) > 1000:
            shares_qqq += delta_eq / qqq_price
            cash -= delta_eq
            current_equity_value = target_equity_value

        target_btc_value = nav * target_btc_pct
        delta_btc = target_btc_value - current_btc_value
        if abs(delta_btc) > 1000:
            shares_btc += delta_btc / btc_price
            cash -= delta_btc
            current_btc_value = target_btc_value

        # 5. Manage PTRH (Addendum 6 + CAM)
        cam_inputs = CamInputs(
            current_equity_pct=current_equity_value / nav,
            regime_score=regime_score,
            fem_concentration_score=0.4, # Mock
            macro_stress_score=row['VIX'] / 100.0,
            cdm_active_signals=0,
            nav=nav
        )
        required_notional = calculate_required_notional(cam_inputs)
        
        # Roll logic
        if ptrh_dte <= 30 or ptrh_contracts == 0:
            # Sell existing
            if ptrh_contracts > 0:
                cash += ptrh_value
                ptrh_contracts = 0
            
            # Buy new
            ptrh_dte = 90
            ptrh_strike = find_strike_for_delta(qqq_price, ptrh_dte/365.0, r, sigma, -0.35)
            opt_price = black_scholes_put(qqq_price, ptrh_strike, ptrh_dte/365.0, r, sigma)
            # Size it
            if opt_price > 0:
                cost_per_contract = opt_price * 100
                ptrh_contracts = max(1, int(required_notional / cost_per_contract))
                cash -= ptrh_contracts * cost_per_contract
                ptrh_value = ptrh_contracts * cost_per_contract
                
        nav = cash + current_equity_value + current_btc_value + current_defensive_value + ptrh_value
            
        # 6. Record State
        history_records.append({
            'Date': date,
            'NAV': nav,
            'QQQ_Price': qqq_price,
            'SPY_Price': row['SPY_CLOSE'],
            'BTC_Price': btc_price,
            'VIX': row['VIX'],
            'HY_Spread': row['HY_SPREAD'],
            'Regime': aras_out.regime,
            'Regime_Score': regime_score,
            'Equity_Ceiling': aras_out.equity_ceiling_pct,
            'PDS_Status': pds_out.status,
            'PDS_Ceiling': pds_out.pds_ceiling,
            'Equity_Pct': current_equity_value / nav,
            'Crypto_Pct': current_btc_value / nav,
            'PTRH_Value': ptrh_value,
            'PTRH_Notional_Target': required_notional / nav,
            'Drawdown': pds_out.drawdown_pct
        })
        
    history_df = pd.DataFrame(history_records)
    history_df.set_index('Date', inplace=True)
    return BacktestResult(history_df)

if __name__ == "__main__":
    res = run_simulation_phase2("2020-01-01", "2020-05-01")
    print(res.history[['NAV', 'Regime', 'Equity_Pct', 'Crypto_Pct', 'Drawdown']].tail())
