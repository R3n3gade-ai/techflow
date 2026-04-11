from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from engine.cdm import CdmAlert
from engine.tdc_state import TdcTickerState


@dataclass
class ThesisSignal:
    ticker: str
    thesis_status: str
    gate3_score: Optional[float]
    source_category: str


@dataclass
class QueueReasoningSignal:
    ticker: str
    reason: str
    action: str
    confidence: str
    note: str


KNOWN_RISK_ON_ONLY = {'NVDA'}
KNOWN_SENTINEL_UNCONFIRMED = {'BE'}
CONSENSUS_PRICED_HINTS = {
    'GEV': 'Power Singularity enthusiasm is already reflected in price / narrative.',
    'CEG': 'Nuclear / AI power demand thesis is treated as consensus-priced.',
    'VST': 'Texas grid + AI demand thesis is widely recognized and no longer clearly pre-consensus.',
    'VRT': 'Business remains valid, but queue size-up asymmetry appears weaker than earlier cycle phase.'
}
PRECONSENSUS_HINTS = {
    'GOOGL': 'Market may still be using the wrong identity to price the asset, preserving Gate 3 asymmetry.'
}


def build_thesis_signal_map(sentinel_records: Dict[str, object]) -> Dict[str, ThesisSignal]:
    out: Dict[str, ThesisSignal] = {}
    for ticker, rec in sentinel_records.items():
        out[ticker.upper()] = ThesisSignal(
            ticker=ticker.upper(),
            thesis_status=getattr(rec, 'status', 'MISSING'),
            gate3_score=getattr(rec, 'gate3_raw_score', None),
            source_category=getattr(rec, 'gate6_source_category', 'None') or 'None',
        )
    return out


def _summarize_alerts_by_ticker(cdm_alerts: List[CdmAlert]) -> Dict[str, List[CdmAlert]]:
    out: Dict[str, List[CdmAlert]] = {}
    for alert in cdm_alerts:
        out.setdefault(alert.ticker.upper(), []).append(alert)
    return out


def _infer_consensus_vs_asymmetry(ticker: str, thesis: Optional[ThesisSignal]) -> Optional[QueueReasoningSignal]:
    t = ticker.upper()
    if t in CONSENSUS_PRICED_HINTS:
        action = 'HOLD' if t == 'VRT' else 'REMOVE'
        return QueueReasoningSignal(
            ticker=t,
            reason='CONSENSUS_PRICED',
            action=action,
            confidence='MEDIUM',
            note=CONSENSUS_PRICED_HINTS[t]
        )

    if t in PRECONSENSUS_HINTS:
        return QueueReasoningSignal(
            ticker=t,
            reason='ASYMMETRY_RETAINED',
            action='KEEP',
            confidence='MEDIUM',
            note=PRECONSENSUS_HINTS[t]
        )

    if thesis and thesis.gate3_score is not None:
        if thesis.gate3_score < 14:
            return QueueReasoningSignal(
                ticker=t,
                reason='SENTINEL_UNCONFIRMED',
                action='REMOVE',
                confidence='MEDIUM',
                note=f'Gate 3 score {thesis.gate3_score} is below Cat A/B threshold 14.'
            )
        return QueueReasoningSignal(
            ticker=t,
            reason='ASYMMETRY_RETAINED',
            action='KEEP',
            confidence='LOW',
            note=f'Gate 3 score {thesis.gate3_score} remains above minimum threshold; asymmetry retained until contradicted by richer valuation logic.'
        )

    return None


def derive_queue_reasoning_signals(
    queue_tickers: List[str],
    thesis_map: Dict[str, ThesisSignal],
    cdm_alerts: List[CdmAlert],
    tdc_state_by_ticker: Optional[Dict[str, TdcTickerState]] = None,
) -> Dict[str, QueueReasoningSignal]:
    """
    Transitional queue-reasoning layer.

    Goal: move queue reasons away from hardcoded report assumptions and toward
    structured thesis/event-derived signals.

    This is still interim. It uses:
    - live thesis status if present
    - propagated CDM alerts if present
    - explicit known queue policies already surfaced by the user's canonical comparison
    """
    alerts_by_ticker = _summarize_alerts_by_ticker(cdm_alerts)
    tdc_state_by_ticker = tdc_state_by_ticker or {}
    out: Dict[str, QueueReasoningSignal] = {}

    for ticker in queue_tickers:
        t = ticker.upper()
        thesis = thesis_map.get(t)
        ticker_alerts = alerts_by_ticker.get(t, [])
        tdc_state = tdc_state_by_ticker.get(t)

        if t in KNOWN_SENTINEL_UNCONFIRMED:
            out[t] = QueueReasoningSignal(
                ticker=t,
                reason='SENTINEL_UNCONFIRMED',
                action='REMOVE',
                confidence='HIGH',
                note='Ticker is explicitly treated as unconfirmed until a valid SENTINEL passage exists.'
            )
            continue

        if t in KNOWN_RISK_ON_ONLY:
            out[t] = QueueReasoningSignal(
                ticker=t,
                reason='RISK_ON_EVAL_ONLY',
                action='EVAL_ONLY',
                confidence='HIGH',
                note='Ticker is treated as eval-only in current governance posture.'
            )
            continue

        if thesis and thesis.thesis_status in {'REJECTED', 'RETIRED'}:
            out[t] = QueueReasoningSignal(
                ticker=t,
                reason='SENTINEL_UNCONFIRMED',
                action='REMOVE',
                confidence='HIGH',
                note=f'Thesis status is {thesis.thesis_status}.'
            )
            continue

        if tdc_state:
            if tdc_state.tis_label == 'BROKEN':
                out[t] = QueueReasoningSignal(
                    ticker=t,
                    reason='THESIS_MONITOR_ONLY',
                    action='REMOVE',
                    confidence='HIGH',
                    note=f"TDC state is BROKEN due to {tdc_state.trigger_entity}; recommended_action={tdc_state.recommended_action}."
                )
                continue
            if tdc_state.tis_label in {'WATCH', 'IMPAIRED'}:
                out[t] = QueueReasoningSignal(
                    ticker=t,
                    reason='THESIS_MONITOR_ONLY',
                    action='MONITOR',
                    confidence='HIGH',
                    note=f"TDC state is {tdc_state.tis_label} due to {tdc_state.trigger_entity}; recommended_action={tdc_state.recommended_action}."
                )
                continue

        if ticker_alerts:
            strongest = sorted(ticker_alerts, key=lambda a: ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'].index(a.severity))[-1]
            out[t] = QueueReasoningSignal(
                ticker=t,
                reason='THESIS_MONITOR_ONLY',
                action='MONITOR',
                confidence='MEDIUM',
                note=f'Active CDM pressure from {strongest.triggering_entity} ({strongest.event_type}, {strongest.severity}).'
            )
            continue

        asymmetry_signal = _infer_consensus_vs_asymmetry(t, thesis)
        if asymmetry_signal:
            out[t] = asymmetry_signal
            continue

        out[t] = QueueReasoningSignal(
            ticker=t,
            reason='REGIME_NOT_CLEARED',
            action='KEEP',
            confidence='LOW',
            note='No definitive thesis/event removal signal yet; keep transitional queue posture.'
        )

    return out
