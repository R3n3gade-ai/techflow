# ARMS Next-Wave Cold Truth Audit — 2026-04-10

## Purpose
This is the next-wave punch list after the first remediation pass.
It identifies the largest remaining placeholder, fallback, bridge-backed, and overclaimed paths still preventing ARMS from matching MJ's canonical architecture at runtime.

---

## Highest-Severity Remaining Code Issues

### 1. `broker_api.py` still contains execution-path scaffold / unsafe fallback behavior
**Severity:** CRITICAL

Observed:
- `connect()` still mutates `IB_AVAILABLE` and falls back to simulated connected mode on connection failure.
- `submit_order()` still contains ugly price fallback behavior including a default divisor around `150.0`.
- `get_order_status()` remains scaffolded and always returns `PENDING`.
- broker docstring still says option contract resolution is mocked/pending even though partial live path exists.

Why this matters:
- execution path cannot contain hidden simulation downgrade or arbitrary arithmetic shortcuts in a real-money architecture.

Required fix:
- remove simulated connected-mode fallback from `connect()`
- formalize price-source policy
- reject execution when price quality is insufficient
- implement real order-status reconciliation
- update docstrings/comments to current truth

---

### 2. `macro_compass.py` still uses opaque LLM event overlay logic
**Severity:** CRITICAL

Observed:
- `_load_event_shock_overlay()` relies on LLM inference of macro/oil/diplomacy/military stress.
- missing signals default to midpoint-ish behavior in some paths.
- no typed event-state model currently drives regime score.

Why this matters:
- L2 regime logic must be auditable and sourced, not partially inferred via hidden prompt overlays.

Required fix:
- replace prompt-derived overlay with typed event-state inputs
- harden signal completeness expectations
- document exact event contribution path

---

### 3. `main.py` still contains transitional monitor scaffolding
**Severity:** HIGH

Observed:
- `score_prior=0.72`
- `next_catalyst='Next Catalyst'`
- decision queue text is remediation/debug text, not portfolio-operating truth
- equity `session_perf` remains `0.0`
- module panel text still generic in places
- macro drivers are generic remediation language instead of actual system-derived state

Why this matters:
- report state is still partially scaffolded and therefore cannot yet match MJ-grade daily truth.

Required fix:
- derive prior score from stored history
- derive catalysts from typed event-state/catalyst layer
- replace temporary PM decision items with actual operating queue
- source session/week performance truthfully

---

### 4. `tail_hedge.py` still depends on partial live market-data assumptions
**Severity:** HIGH

Observed:
- import style and broker coupling are still rough
- options chain logic exists, but market-data dependency remains fragile
- true no-subscription handling and alternate contract discovery path are not fully institutionalized

Why this matters:
- PTRH is core infrastructure. Partial chain quality is unacceptable.

Required fix:
- formalize live/delayed/no-data policy
- isolate chain qualification and Greeks acquisition cleanly
- eliminate ambiguous failure paths

---

### 5. Daily monitor HTML view stack is stale / mock-oriented
**Severity:** HIGH

Observed:
- `daily_monitor_view.py` is still explicitly loading `mj_pm_notes.json`, `mj_portfolio_snapshot.json`, and `mj_strategic_queue.json`
- hardcoded dates and narrative framing remain
- renderer layout reflects old mock report fabrication path

Why this matters:
- this entire path is dangerous if mistaken for current truth.

Required fix:
- mark it explicitly as deprecated transitional artifact or rebuild it on typed monitor state
- do not allow it to masquerade as authoritative monitor generation

---

## Medium-Severity Remaining Code Issues

### 6. TDC weekly audit still stubbed
**Severity:** MEDIUM-HIGH
- `run_weekly_tdc_audit()` remains placeholder
- no broad recurring thesis integrity sweep yet

### 7. Queue reasoning still contains transitional ticker-specific heuristics
**Severity:** MEDIUM-HIGH
- better than before, but still not full live derived asymmetry logic
- must be replaced by real consensus / asymmetry evaluator

### 8. Queue state transitions are not yet persisted as first-class audit state
**Severity:** MEDIUM
- queue governance changes should be durable and auditable

### 9. `main.py` still uses rough proxies in multiple modules
**Severity:** MEDIUM
Examples:
- AUP uses hardcoded proxy inputs
- SLOF current leverage uses `1.0 proxy`
- incapacitation last heartbeat uses synthetic `45 minutes ago`
- some FEM / bridge values still use simplified state

### 10. Equity/session performance computation is not yet real
**Severity:** MEDIUM
- monitor still uses `session_perf: 0.0`
- no weekly performance table feeding output

---

## Documentation Problems Still Remaining

### 1. More implementation-status docs remain misleading
Still needing historical/non-authoritative labels:
- `docs/ARMS_IMPLEMENTATION_STATUS_DATA_PIPELINES.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_INTELLIGENCE.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_DAILY_MONITOR.md`
- likely other sprint-complete docs in same family

### 2. Some status docs are now directly contradicted by code reality
Examples:
- `ARMS_IMPLEMENTATION_STATUS_DATA_PIPELINES.md` claims Yahoo Finance live integration that is not the current runtime truth path
- `ARMS_IMPLEMENTATION_STATUS_INTELLIGENCE.md` claims graceful degradation via local JSON generation, which is now explicitly contrary to fail-loud live intent
- `ARMS_IMPLEMENTATION_STATUS_DAILY_MONITOR.md` describes upgraded HTML path, but current truthful path is markdown + typed state in transition

### 3. Duplicate docs still need reconciliation
- duplicate naming variants remain throughout docs folder
- canonical-vs-supporting-vs-historical split still needs broader cleanup

---

## Priority Order for Next Remediation Wave
1. **Broker API hardening**
2. **Macro Compass event-state replacement**
3. **Main orchestrator report-state cleanup**
4. **Deprecate / label stale daily monitor HTML/mock path**
5. **Label remaining misleading implementation-status docs**
6. **Persistent queue governance audit trail**
7. **Real TDC weekly audit**

---

## Bottom Line
The system is materially cleaner than before this remediation push.
But the largest remaining threats are now concentrated in:
- execution truth
- regime/event truth
- monitor-state truth
- stale docs overstating readiness

Those are the next targets.
