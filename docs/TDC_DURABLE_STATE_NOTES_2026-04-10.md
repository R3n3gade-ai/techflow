# TDC Durable State Notes — 2026-04-10

## What changed
TDC is no longer only a one-off review function that prints/logs a result.
It now persists ticker-level thesis integrity state to:
- `achelion_arms/state/tdc_state.json`

This state is now available to queue reasoning and therefore can influence:
- remove
- monitor
- hold/avoid queue progression

## Why it matters
Before this change:
- CDM/TDC could detect a problem
- a review could be produced
- but the queue did not have a durable control input from that result

After this change:
- queue reasoning can consume durable TIS state
- BROKEN -> remove path exists
- WATCH / IMPAIRED -> monitor path exists

## Remaining gaps
1. TDC still uses simplified source thesis context and should pull full SENTINEL records
2. queue reasoning should eventually persist its own state transitions for auditability
3. monitor/report should expose TDC-driven queue downgrades explicitly
4. weekly TDC audit still needs implementation
