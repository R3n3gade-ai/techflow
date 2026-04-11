from __future__ import annotations

from dataclasses import dataclass
from typing import List

from engine.cdm import NewsItem


@dataclass
class MacroEventState:
    macro_stress_score: float = 0.0
    oil_stress_score: float = 0.0
    diplomacy_breakdown_score: float = 0.0
    military_escalation_score: float = 0.0
    override_floor: float = 0.0
    rationale: List[str] = None

    def __post_init__(self):
        if self.rationale is None:
            self.rationale = []


def _clip(x: float) -> float:
    return max(0.0, min(1.0, x))


def derive_macro_event_state(events: List[NewsItem]) -> MacroEventState:
    """
    Transitional typed event-state derivation.

    Replaces opaque LLM overlay behavior with explicit heuristic event mapping.
    This is not the final institutional event-state engine, but it is auditable,
    deterministic, and sourced from ingested events.
    """
    state = MacroEventState()

    for event in events:
        headline = f"{event.headline} {event.content}".lower()
        ev = event.event_type.upper()

        if ev in {'LEGAL_RULING', 'REGULATORY_FILING', 'CREDIT_EVENT'}:
            state.macro_stress_score = max(state.macro_stress_score, 0.35)
            state.rationale.append(f"{event.event_type} -> macro stress")

        if any(term in headline for term in ['oil', 'brent', 'wti', 'hormuz', 'shipping lane', 'tanker']):
            state.oil_stress_score = max(state.oil_stress_score, 0.45)
            state.rationale.append(f"{event.headline[:80]} -> oil stress")

        if any(term in headline for term in ['talks collapse', 'ceasefire fracture', 'iran walks', 'negotiation breakdown']):
            state.diplomacy_breakdown_score = max(state.diplomacy_breakdown_score, 0.60)
            state.rationale.append(f"{event.headline[:80]} -> diplomacy breakdown")
        elif any(term in headline for term in ['talks', 'delegation', 'ceasefire', 'framework agreed', 'productive talks']):
            state.diplomacy_breakdown_score = max(state.diplomacy_breakdown_score, 0.15)
            state.rationale.append(f"{event.headline[:80]} -> diplomacy watch")

        if any(term in headline for term in ['missile', 'strike', 'military', 'attack', 'retaliation', 'drone']):
            state.military_escalation_score = max(state.military_escalation_score, 0.60)
            state.rationale.append(f"{event.headline[:80]} -> military escalation")

    weighted = (
        state.macro_stress_score * 0.35 +
        state.oil_stress_score * 0.25 +
        state.diplomacy_breakdown_score * 0.20 +
        state.military_escalation_score * 0.20
    )
    state.override_floor = _clip(weighted)
    state.macro_stress_score = _clip(state.macro_stress_score)
    state.oil_stress_score = _clip(state.oil_stress_score)
    state.diplomacy_breakdown_score = _clip(state.diplomacy_breakdown_score)
    state.military_escalation_score = _clip(state.military_escalation_score)
    return state
