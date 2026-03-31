"""
ACHELION ARMS v1.1 - FULL INTEGRATION CYCLE
"Silence is trust in the architecture."

This script executes a complete ARMS operational cycle, integrating all 
Phase 1, 2, and 3 modules. It simulates the 6:00 AM CT sweep.
"""

import datetime
import json
from typing import List, Dict, Any

# --- 1. Core Services & Interfaces ---
from data_feeds.pipeline import DataPipeline
from execution.broker_api import IBKRBroker
from execution.confirmation_queue import ConfirmationQueue, QueuedAction
from reporting.audit_log import SessionLogEntry, append_to_log
from execution.interfaces import OrderRequest

# --- 2. Engine Modules ---
from engine.mics import calculate_mics, SentinelGateInputs
from engine.cam import CamInputs, calculate_required_notional
from engine.tail_hedge import run_ptrh_module, OptionsPosition
from engine.dshp import run_dshp_check, DefensivePosition
from engine.cdm import run_cdm_scan, NewsItem
from engine.tdc import run_thesis_review
from engine.regime_probability import calculate_rpe
from engine.ares import run_ares_check
from engine.cdf import calculate_position_decay
from engine.mc_rss import calculate_mc_rss
from engine.incapacitation import run_incapacitation_check
from engine.asymmetric_upside import run_aup_check
from reporting.daily_monitor import generate_daily_monitor

def run_full_arms_cycle():
    log_file = "achelion_arms/logs/session_log.jsonl"
    now = datetime.datetime.now(datetime.timezone.utc)
    
    print("\n" + "="*60)
    print("ACHELION ARMS v1.1 - FULL OPERATIONAL SWEEP")
    print(f"Cycle Initiated: {now.isoformat()}")
    print("="*60)
    
    # --- PHASE 0: INITIALIZATION ---
    print("\n[STEP 0] Initializing ARMS Services...")
    data_pipeline = DataPipeline()
    broker = IBKRBroker()
    confirmation_queue = ConfirmationQueue()
    broker.connect()
    
    append_to_log(SessionLogEntry(
        timestamp=now.isoformat(), 
        action_type='CYCLE_START', 
        triggering_module='MAIN_ORCHESTRATOR', 
        triggering_signal='Full integration sweep initiated.'
    ))

    # --- PHASE 1: DATA INGESTION (THE SENSES) ---
    print("\n[STEP 1] Running Multi-Feed Data Ingestion...")
    signals = data_pipeline.run_all_feeds()
    # Extract specific values for downstream engines
    # (Simulating extraction from SignalRecord list)
    vix_val = 14.5
    sp_pmi = 0.515
    btc_funding = 0.0001
    
    # --- PHASE 2: MACRO & SENTIMENT (ARAS / RPE / RSS) ---
    print("\n[STEP 2] Calculating Regime & Sentiment...")
    # 2.1 RSS (Retail Sentiment)
    rss_res = calculate_mc_rss(
        retail_net_buying_usd=1.2e9, 
        retail_history_30d=[1.1e9, 1.3e9], 
        naaim_exposure_index=85.0, 
        aaii_bull_bear_spread=0.20
    )
    
    # 2.2 RPE (Regime Probability)
    rpe_res = calculate_rpe(current_regime="WATCH", latest_signals=signals)
    
    # 2.3 Incapacitation Check (Safety)
    last_hb = now - datetime.timedelta(minutes=45)
    incap_res = run_incapacitation_check(last_hb, "WATCH")
    
    # --- PHASE 3: PORTFOLIO MAINTENANCE (CDF / DSHP) ---
    print("\n[STEP 3] Auditing Portfolio & Performance...")
    # 3.1 DSHP (Harvesting)
    nav = 50_000_000.0
    mock_sleeve = {
        'SGOL': DefensivePosition('SGOL', nav * 0.025, nav * 0.02, 0.025) # 25% app
    }
    harvest_actions = run_dshp_check(mock_sleeve, nav)
    
    # 3.2 CDF (Decay)
    cdf_status = [calculate_position_decay("TSLA", 10, 2.0)] # Normal
    
    # --- PHASE 4: HEDGE MANAGEMENT (CAM / PTRH) ---
    print("\n[STEP 4] Calculating Tail-Risk Coverage...")
    cam_in = CamInputs(
        current_equity_pct=0.58, regime_score=0.35, 
        fem_concentration_score=0.45, macro_stress_score=0.25, 
        cdm_active_signals=0, nav=nav
    )
    mock_puts = [OptionsPosition("QQQ", "PUT", 480, "2026-05-15", 100, 600_000)]
    ptrh_res = run_ptrh_module(cam_in, mock_puts)
    
    # --- PHASE 5: THESIS INTEGRITY (CDM / TDC) ---
    print("\n[STEP 5] Running AI-Driven Thesis Audits...")
    mock_news = [NewsItem(
        'SEC_EDGAR', 'Alphabet CEO Files Form 4', 'Insider selling detected...', 
        now.isoformat(), ['Alphabet'], 'INSIDER_SALE'
    )]
    cdm_alerts = run_cdm_scan(mock_news)
    tdc_results = []
    for alert in cdm_alerts:
        tdc_results.append(run_thesis_review(alert))
        
    # --- PHASE 6: GROWTH & RE-ENTRY (ARES / AUP) ---
    print("\n[STEP 6] Evaluating Growth & Re-Entry...")
    ares_res = run_ares_check("WATCH", 0.35, 0.25, rss_res.composite_rss)
    aup_res = run_aup_check("WATCH", 7.8, True, 0.15, 0.05)
    
    # --- PHASE 7: CONSOLIDATION & REPORTING ---
    print("\n[STEP 7] Generating Daily Monitor v2.1...")
    # Mock some data for the monitor aggregator
    mics_results = {"NVDA": calculate_mics(SentinelGateInputs(24, 'Cat B', 'NORMAL', 'WATCH'))}
    
    # Actually add harvest actions to confirmation queue for simulation
    for ha in harvest_actions:
        confirmation_queue.add_action(ha)
        
    monitor = generate_daily_monitor(
        current_regime="WATCH", regime_score=0.35, rpe_signal=rpe_res,
        ptrh_status=ptrh_res, mics_results=mics_results,
        tdc_results=tdc_results, cdm_alerts=[a.__dict__ for a in cdm_alerts],
        dshp_actions=[ha.item.__dict__ for ha in harvest_actions], # Simplified for mock
        ares_status=ares_res, cdf_statuses=cdf_status,
        rss_result=rss_res, safety_status=incap_res, nav=nav
    )
    
    print("\n" + "="*60)
    print("SWEEP COMPLETE: MONITOR PAYLOAD READY")
    print(f"Decision Queue Size: {len(monitor.decision_queue)}")
    print(f"Current Regime: {monitor.regime} (Score: {monitor.regime_score})")
    print(f"Anticipatory Signal: {monitor.rpe.highest_prob_transition} ({monitor.rpe.highest_prob_value:.1%})")
    print("="*60)
    
    append_to_log(SessionLogEntry(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), 
        action_type='CYCLE_END', 
        triggering_module='MAIN_ORCHESTRATOR', 
        triggering_signal='Daily sweep complete.'
    ))
    
    broker.disconnect()

if __name__ == '__main__':
    run_full_arms_cycle()
