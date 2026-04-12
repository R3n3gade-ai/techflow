> **? STALE DOCUMENT — NOT AUTHORITATIVE**
> This document predates significant code changes (April 2026 remediation cycle).
> For current system truth, see: ARMS_NEXT_WAVE_COLD_TRUTH_AUDIT_2026-04-10.md
> and ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md

# HTML Monitor Path Deprecation â€” 2026-04-10

## Status
The following files are deprecated transitional artifacts and must not be treated as authoritative runtime monitor generation:
- `src/reporting/daily_monitor_view.py`
- `src/reporting/daily_monitor_renderer.py`

## Why
These files:
- load static MJ snapshot/note files
- contain hardcoded dates / labels / narrative assumptions
- were built around mock-era layout parity rather than typed runtime state

## Rule
Do not use the HTML monitor path as proof of live monitor correctness.
The active truthful path is:
- typed state in `src/reporting/monitor_state.py`
- markdown generation in `src/reporting/daily_monitor.py`
- orchestration in `src/main.py`

## Future
If HTML/PDF output is desired later, rebuild it on top of typed monitor state only.
Do not revive the old snapshot-driven path.
