# Queue Governance Persistence — 2026-04-10

## What changed
Queue governance is no longer only an in-memory run artifact.
A durable queue snapshot is now persisted to:
- `achelion_arms/state/queue_governance_state.json`

A queue diff is computed every cycle and transitions are logged to the immutable session log as:
- `QUEUE_STATE_CHANGE`

## Why this matters
Before this change:
- queue state existed only inside the current run
- removed/monitor/hold transitions were not durable
- there was no stable audit trail of queue governance evolution

After this change:
- queue posture persists across cycles
- changes in state/reason are logged
- the next dev can inspect the durable queue snapshot directly

## Remaining gaps
1. queue persistence is still storing transitional reasoning outputs, not final canonical asymmetry intelligence
2. historical multi-snapshot queue timeline/reporting is still basic
3. queue transition data is not yet surfaced richly in the monitor narrative
