"""
ARMS Engine: SENTINEL Bridge

Truthful interim bridge for live MICS inputs.
Loads per-ticker SENTINEL gate records from a local JSON file specified by
ARMS_SENTINEL_JSON.
"""

import json
import os
from dataclasses import dataclass
from typing import Dict, Optional

from engine.mics import SentinelGateInputs
from engine.bridge_paths import bridge_path


@dataclass
class SentinelRecord:
    ticker: str
    gate3_raw_score: float
    source_category: str
    fem_impact: str
    regime_at_entry: str


def load_sentinel_records() -> Dict[str, SentinelRecord]:
    path = bridge_path('ARMS_SENTINEL_JSON', 'sentinel_records.json')
    if not os.path.exists(path):
        print(f"[SentinelBridge] SENTINEL bridge file not found: {path}")
        return {}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except Exception as e:
        print(f"[SentinelBridge] Failed to read SENTINEL JSON: {e}")
        return {}

    if not isinstance(payload, list):
        print("[SentinelBridge] SENTINEL JSON must be a list of records.")
        return {}

    records: Dict[str, SentinelRecord] = {}
    for row in payload:
        try:
            rec = SentinelRecord(
                ticker=str(row['ticker']).upper(),
                gate3_raw_score=float(row['gate3_raw_score']),
                source_category=str(row['source_category']),
                fem_impact=str(row['fem_impact']),
                regime_at_entry=str(row['regime_at_entry'])
            )
            records[rec.ticker] = rec
        except Exception as e:
            print(f"[SentinelBridge] Skipping invalid SENTINEL row: {e}")
    return records


def build_mics_input_for_ticker(ticker: str, current_regime: str, fallback_fem_impact: str = 'NORMAL->NORMAL') -> SentinelGateInputs:
    records = load_sentinel_records()
    rec: Optional[SentinelRecord] = records.get(ticker.upper())
    if rec:
        return SentinelGateInputs(
            gate3_raw_score=rec.gate3_raw_score,
            source_category=rec.source_category,  # type: ignore[arg-type]
            fem_impact=rec.fem_impact,
            regime_at_entry=rec.regime_at_entry
        )

    # Truthful fallback: still explicit and deterministic, but lower-conviction than a true SENTINEL record.
    return SentinelGateInputs(
        gate3_raw_score=14.0,
        source_category='None',
        fem_impact=fallback_fem_impact,
        regime_at_entry=current_regime if current_regime in {'RISK_ON', 'WATCH', 'NEUTRAL'} else 'NEUTRAL'
    )
