from __future__ import annotations

import datetime
import json
import os
from dataclasses import asdict, dataclass
from typing import Dict, List

from engine.bridge_paths import bridge_path
from execution.queue_state import QueueGovernanceEntry, QueueGovernanceState
from reporting.audit_log import SessionLogEntry, append_to_log


QUEUE_STATE_PATH = bridge_path('ARMS_QUEUE_STATE_JSON', 'queue_governance_state.json')


@dataclass
class QueueTransition:
    ticker: str
    old_state: str
    new_state: str
    old_reason: str
    new_reason: str
    changed_at: str
    note: str


@dataclass
class PersistedQueueSnapshot:
    updated_at: str
    headline_status: str
    entries: Dict[str, dict]


def _flatten_state(state: QueueGovernanceState) -> Dict[str, QueueGovernanceEntry]:
    out: Dict[str, QueueGovernanceEntry] = {}
    for entry in state.neutral_queue + state.risk_on_queue + state.removed_items + state.monitor_list:
        out[entry.ticker.upper()] = entry
    return out


def load_queue_snapshot() -> PersistedQueueSnapshot:
    if not os.path.exists(QUEUE_STATE_PATH):
        return PersistedQueueSnapshot(updated_at='', headline_status='UNKNOWN', entries={})
    try:
        with open(QUEUE_STATE_PATH, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        return PersistedQueueSnapshot(
            updated_at=raw.get('updated_at', ''),
            headline_status=raw.get('headline_status', 'UNKNOWN'),
            entries=raw.get('entries', {}),
        )
    except Exception as e:
        print(f"[QueuePersistence] Failed to load queue snapshot: {e}")
        return PersistedQueueSnapshot(updated_at='', headline_status='UNKNOWN', entries={})


def diff_queue_state(previous: PersistedQueueSnapshot, current: QueueGovernanceState) -> List[QueueTransition]:
    transitions: List[QueueTransition] = []
    previous_entries = previous.entries or {}
    current_entries = _flatten_state(current)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    all_tickers = sorted(set(previous_entries.keys()) | set(current_entries.keys()))
    for ticker in all_tickers:
        old = previous_entries.get(ticker)
        new = current_entries.get(ticker)

        old_state = old.get('state', 'ABSENT') if old else 'ABSENT'
        old_reason = old.get('reason', 'ABSENT') if old else 'ABSENT'
        new_state = new.state if new else 'ABSENT'
        new_reason = new.reason if new else 'ABSENT'

        if old_state != new_state or old_reason != new_reason:
            note = new.notes if new else 'Ticker removed from current queue snapshot.'
            transitions.append(QueueTransition(
                ticker=ticker,
                old_state=old_state,
                new_state=new_state,
                old_reason=old_reason,
                new_reason=new_reason,
                changed_at=now_iso,
                note=note,
            ))

    return transitions


def persist_queue_state(state: QueueGovernanceState) -> List[QueueTransition]:
    previous = load_queue_snapshot()
    transitions = diff_queue_state(previous, state)
    current_entries = _flatten_state(state)

    payload = {
        'updated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'headline_status': state.headline_status,
        'entries': {ticker: asdict(entry) for ticker, entry in current_entries.items()},
    }

    os.makedirs(os.path.dirname(QUEUE_STATE_PATH), exist_ok=True)
    with open(QUEUE_STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

    for tr in transitions:
        append_to_log(SessionLogEntry(
            timestamp=tr.changed_at,
            action_type='QUEUE_STATE_CHANGE',
            triggering_module='QUEUE_GOVERNANCE',
            triggering_signal=f"{tr.ticker}: {tr.old_state}/{tr.old_reason} -> {tr.new_state}/{tr.new_reason}. {tr.note}",
            ticker=tr.ticker,
        ))

    return transitions
