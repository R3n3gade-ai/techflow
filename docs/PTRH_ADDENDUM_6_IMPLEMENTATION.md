# PTRH Addendum 6 Implementation

## Objective
Implement Phase 1 of the PTRH Adaptive Strike Protocol (ARMS-ADD-006).

## Scope
- Update `broker_api.py` to request live option chains and Greeks (Delta, Bid/Ask spread, Open Interest) for a given underlying.
- Rewrite `tail_hedge.py` strike selection logic.
- Implement the Delta-Primary target (-0.35 midpoint).
- Implement Gate 1 (Standard) and Gate 4 (Abort).
- Generate a single pre-validated execution ticket (no PM comparison list).
- Log the selected parameters.

## Out of Scope (Phase 2+)
- Drift detection tracking over 30 days.
- Full 4-gate fallback resolution (Gate 2 and Gate 3 will be stubbed or built if time permits, but Phase 1 only strictly requires Standard and Abort).
- IV regime shift recalibration.
