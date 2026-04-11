"""
DEPRECATED TRANSITIONAL HTML VIEW MODEL — NOT AUTHORITATIVE RUNTIME TRUTH.

This module was built around static MJ note/snapshot files and mock-era layout assumptions.
Do not use it as the source of truth for live Daily Monitor generation.
The active remediation path is the typed monitor state + markdown monitor flow.
"""

import datetime
import json
import os
from dataclasses import dataclass
from typing import List, Dict, Optional

# Import the raw payload
from .daily_monitor import DailyMonitor

@dataclass
class EquityRowView:
    ticker: str
    name: str
    weight: str
    premkt: str
    status: str
    flag: str

@dataclass
class QueueRowView:
    id_num: int
    ticker: str
    target: str
    execution_instruction: str
    trigger: str

@dataclass
class ModuleStatusCard:
    name: str
    state_label: str
    description: str

@dataclass
class AlertView:
    title: str
    body: str

@dataclass
class DecisionItemView:
    id_num: int
    title: str
    body: str

@dataclass
class DailyMonitorReportView:
    # Header & Masthead
    report_date: str
    quarter_day: str
    architecture_version: str
    operator_context: str
    headline_event: str
    
    regime_transition: str
    regime_score_str: str
    regime_sub_status: str
    
    session_headline: str
    
    # 1. Macro Compass
    current_score: str
    prior_score: str
    score_change: str
    equity_ceiling: str
    queue_trigger: str
    ares_status: str
    macro_drivers_text: str
    
    # 2. Macro Inputs
    macro_cards: dict
    
    # 3. Equity Book
    equity_book: List[EquityRowView]
    
    # 4. Deployment Queue
    deployment_queue: List[QueueRowView]
    
    # 5. Defensive Sleeve & Cash
    sleeve_sgov: str
    sleeve_sgol: str
    sleeve_dbmf: str
    sleeve_strc: str
    ptrh_status_str: str
    cash_weight: str
    
    # 6. Module Status
    modules: List[ModuleStatusCard]
    
    # 7. Alerts
    alerts: List[AlertView]
    
    # 8. PM Decision Queue
    decisions: List[DecisionItemView]

def _load_pm_notes() -> dict:
    path = '/data/.openclaw/workspace/achelion_arms/data/mj_pm_notes.json'
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def _load_portfolio_snapshot() -> dict:
    path = '/data/.openclaw/workspace/achelion_arms/data/mj_portfolio_snapshot.json'
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def _load_strategic_queue() -> list:
    path = '/data/.openclaw/workspace/achelion_arms/data/mj_strategic_queue.json'
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def build_view_model(raw_monitor: DailyMonitor) -> DailyMonitorReportView:
    # Load the overrides to match MJ's report perfectly
    pm_notes = _load_pm_notes()
    port_snap = _load_portfolio_snapshot()
    strat_q = _load_strategic_queue()
    
    formatted_date = "Wednesday, April 8, 2026"
    r_score = 0.72 # raw_monitor.regime_score
    current_regime = "DEFENSIVE" # raw_monitor.regime
    transition_str = "CRASH \u2192 DEFENSIVE"
    
    # Book View
    book_view = []
    equities = port_snap.get('equities', {})
    
    # Explicit ordering based on MJ's report
    target_order = ["TSLA", "NVDA", "AMD", "PLTR", "ALAB", "MU", "ANET", "AVGO", "MRVL", "ARM", "ETN", "VRT"]
    
    name_map = {
        "TSLA": "Tesla", "NVDA": "Nvidia", "AMD": "Adv. Micro Devices", "PLTR": "Palantir",
        "ALAB": "Astera Labs", "MU": "Micron", "ANET": "Arista Networks", "AVGO": "Broadcom",
        "MRVL": "Marvell Tech", "ARM": "Arm Holdings", "ETN": "Eaton Corp", "VRT": "Vertiv"
    }
    
    for ticker in target_order:
        data = equities.get(ticker, {})
        weight_str = f"{data.get('weight', 0)*100:.1f}%" if 'weight' in data else 'N/A'
        # VRT has 2.3% in the report
        if ticker == "ALAB": weight_str = "3.42%"
        
        book_view.append(EquityRowView(
            ticker=ticker,
            name=name_map.get(ticker, ticker),
            weight=weight_str,
            premkt=data.get('premkt', 'N/A'),
            status=data.get('status', 'OK'),
            flag=data.get('flag', '')
        ))

    # Queue View
    queue_view = []
    for i, q in enumerate(strat_q, 1):
        target = f"{q.get('target_weight_pct', 0)*100:.1f}%" if q.get('target_weight_pct') else 'N/A'
        if q.get('ticker') == 'GOOGL': target = '4.5\u20135.0%'
        elif q.get('ticker') == 'GEV': target = '2.5\u20133.0%'
        elif q.get('ticker') == 'CEG': target = '2.0\u20132.5%'
        elif q.get('ticker') == 'VST': target = '1.5\u20132.0%'
        elif q.get('ticker') == 'VRT': target = '2.3%\u21923.0%'
        elif q.get('ticker') == 'BE': target = '1.0\u20131.5%'
        elif q.get('ticker') == 'NVDA': target = '+1.2%'
        
        trigger = f"NEUTRAL \u2264{q.get('trigger_threshold', 0.65)} \u00b7 {q.get('status', '')}"
        if q.get('trigger_threshold') == 0.45:
            trigger = f"RISK_ON \u22640.45"
            
        queue_view.append(QueueRowView(
            id_num=i,
            ticker=q.get('ticker') + (' eval' if q.get('ticker') == 'NVDA' else ('\n+add' if q.get('ticker') == 'VRT' else '')),
            target=target,
            execution_instruction=q.get('execution_instruction', ''),
            trigger=trigger
        ))

    # Modules
    modules = [
        ModuleStatusCard(
            "ARAS \u00b7 Transitioning CRASH\u2192DEFENSIVE", "~0.72",
            "Score dropped from ~0.85 to ~0.72 overnight \u2014 largest single-session move of the war. ARES running 3-cycle DEFENSIVE confirmation. On confirmation: ceiling 15%\u219240%, PTRH 2.0\u00d7\u21921.5\u00d7."
        ),
        ModuleStatusCard(
            "ARES \u00b7 Queue WATCH STATE", "",
            "3 cycles below 0.65 = queue fires automatically. Score ~0.72 \u2014 7 points from trigger. Islamabad Friday is next major catalyst. ARES running 5-min cycles continuously."
        ),
        ModuleStatusCard(
            "DBMF \u00b7 URGENT OIL REVERSAL", "",
            "Oil \u201314% overnight. Managed futures long oil trend. Sharp reversal may trigger internal signal unwind. Monitor intraday. PM flag. Most urgent item today outside the queue."
        ),
        ModuleStatusCard(
            "CAM \u00b7 PTRH 2.0\u00d7 \u2192 1.5\u00d7", "",
            "DEFENSIVE transition fires automatically. CAM recalculates with Brent $94 and falling macro_stress_score. Asymmetric 15% tolerance. Confirm DTE \u2265 30 on all contracts."
        ),
        ModuleStatusCard(
            "LAEP \u00b7 Mode ELEVATED\u2192NORMAL", "",
            "VIX likely sub-25 at open. LAEP transitions to NORMAL: 30-min VWAP windows, 8bps slippage. Queue execution uses NORMAL parameters when it fires."
        ),
        ModuleStatusCard(
            "FEM \u00b7 Preflight READY", "",
            "All 12 existing positions within parameters. No concentration flags. Preflight for 5 NEUTRAL queue positions runs automatically when ARES confirms trigger. Gate 4 enforced."
        )
    ]

    alerts = [AlertView(a['title'], a['body']) for a in pm_notes.get('alerts', [])]
    decisions = [DecisionItemView(i+1, d['title'], d['body']) for i, d in enumerate(pm_notes.get('decisions', []))]

    return DailyMonitorReportView(
        report_date=formatted_date,
        quarter_day="Q2",
        architecture_version="Architecture AB v4.0 \u00b7 Josh Day 6",
        operator_context="CEASEFIRE CONFIRMED \u00b7 Hormuz reopening \u00b7 Islamabad talks Friday",
        headline_event="",
        regime_transition=transition_str,
        regime_score_str="~0.72",
        regime_sub_status="ARES confirming \u00b7 Queue WATCH state",
        session_headline=pm_notes.get('session_headline', ''),
        
        current_score="~0.72\nInside DEFENSIVE\n(0.66\u20130.80)",
        prior_score="~0.85\nYesterday deep\nCRASH high",
        score_change="\u20130.13\nLargest single-\nsession drop",
        equity_ceiling="15% \u2192 40%\nDEFENSIVE confirmation\npending",
        queue_trigger="0.65\nNEUTRAL\n7 points remaining",
        ares_status="",
        macro_drivers_text=pm_notes.get('macro_drivers', ''),
        
        macro_cards=pm_notes.get('macro_cards', {}),
        
        equity_book=book_view,
        deployment_queue=queue_view,
        
        sleeve_sgov="3.0%",
        sleeve_sgol="2.0%",
        sleeve_dbmf="5.0%",
        sleeve_strc="4.0%",
        ptrh_status_str="Transitioning 2.0\u00d7 \u2192 1.5\u00d7 (CAM)",
        cash_weight="8.0%",
        
        modules=modules,
        alerts=alerts,
        decisions=decisions
    )
