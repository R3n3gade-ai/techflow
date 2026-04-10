"""
ARMS Engine: Macro Compass (L2)

Calculates the Macro Regime Score (0.0 to 1.0) from incoming data pipeline
signals plus an optional event-shock bridge. The event-shock bridge is the
interim path toward MJ's documented geopolitical/oil/diplomacy-aware regime
architecture.
"""

import json
import os
from typing import List

from data_feeds.interfaces import SignalRecord
from engine.bridge_paths import bridge_path


def _extract_raw(signals: List[SignalRecord], signal_type: str, default: float) -> float:
    for s in signals:
        if s.signal_type == signal_type:
            return float(s.raw_value if s.raw_value is not None else s.value)
    return default


def _load_event_shock_overlay(live_news_context: str = "") -> float:
    """
    Replaces the interim JSON bridge with full autonomous LLM inference.
    Evaluates macro stress, oil stress, diplomacy, and military escalation 
    directly from live news events.
    """
    if not live_news_context or "No major market events" in live_news_context:
        return 0.0
        
    from intelligence.llm_wrapper import llm_wrapper
    prompt = f"""
    You are the ARMS Macro Compass Event Assessor.
    Analyze the following live market news and assign a stress score from 0.0 to 1.0 
    for each of the following four vectors.
    
    1. macro_stress_score (General economic/market panic)
    2. oil_stress_score (Energy supply chain disruption)
    3. diplomacy_breakdown_score (Failure of international negotiations)
    4. military_escalation_score (Active kinetic conflict expanding)
    
    CONTEXT:
    {live_news_context}
    
    Return ONLY valid JSON.
    Format: {{"macro_stress_score": 0.0, "oil_stress_score": 0.0, "diplomacy_breakdown_score": 0.0, "military_escalation_score": 0.0}}
    """
    
    try:
        response_json = llm_wrapper.call(task_type='macro_event_inference', prompt=prompt)
        
        if response_json.startswith("```json"):
            response_json = response_json[7:-3].strip()
        elif response_json.startswith("```"):
            response_json = response_json[3:-3].strip()
            
        payload = json.loads(response_json)
        
        macro_stress = float(payload.get('macro_stress_score', 0.0))
        oil_stress = float(payload.get('oil_stress_score', 0.0))
        diplomacy = float(payload.get('diplomacy_breakdown_score', 0.0))
        escalation = float(payload.get('military_escalation_score', 0.0))

        overlay = (
            (macro_stress * 0.35) +
            (oil_stress * 0.25) +
            (diplomacy * 0.20) +
            (escalation * 0.20)
        )
        print(f"[MacroCompass] Autonomous Event Overlay Computed: {overlay:.2f} (Macro:{macro_stress}, Oil:{oil_stress}, Dip:{diplomacy}, Mil:{escalation})")
        return max(0.0, min(1.0, overlay))
    except Exception as e:
        print(f"[MacroCompass] Failed autonomous event inference: {e}")
        return 0.0


def _load_override_floor() -> float:
    path = bridge_path('ARMS_MACRO_EVENT_JSON', 'macro_event_overlay.json')
    if not os.path.exists(path):
        return 0.0
    try:
        with open(path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
        return max(0.0, min(1.0, float(payload.get('override_floor', 0.0) or 0.0)))
    except Exception:
        return 0.0


def calculate_macro_regime_score(signals: List[SignalRecord], live_news_context: str = "") -> float:
    """
    Computes a broader macro regime score from sourced inputs.

    Inputs currently used:
    - VIX
    - HY credit spreads
    - PMI
    - 10Y Treasury yield
    - optional event/oil/diplomacy/military overlay via ARMS_MACRO_EVENT_JSON
    """
    if not signals:
        return 0.50

    vix = _extract_raw(signals, 'VIX_INDEX', 20.0)
    hy_spread = _extract_raw(signals, 'HY_CREDIT_SPREAD', 4.0)
    pmi = _extract_raw(signals, 'PMI_NOWCAST', 50.0)
    ten_y = _extract_raw(signals, '10Y_TREASURY_YIELD', 4.0)

    # Core stress normalization
    v_stress = max(0.0, min(1.0, (vix - 10.0) / 35.0))
    h_stress = max(0.0, min(1.0, (hy_spread - 3.0) / 5.0))
    p_stress = max(0.0, min(1.0, (55.0 - pmi) / 10.0))
    y_stress = max(0.0, min(1.0, (ten_y - 3.5) / 2.0))

    base_score = (
        (v_stress * 0.30) +
        (h_stress * 0.30) +
        (p_stress * 0.20) +
        (y_stress * 0.20)
    )

    overlay = _load_event_shock_overlay(live_news_context)
    score = max(base_score, _load_override_floor())
    score = max(score, overlay)

    return max(0.0, min(1.0, score))


def get_regime_label(score: float) -> str:
    if score <= 0.30:
        return "RISK_ON"
    if score <= 0.50:
        return "WATCH"
    if score <= 0.65:
        return "NEUTRAL"
    if score <= 0.80:
        return "DEFENSIVE"
    return "CRASH"
