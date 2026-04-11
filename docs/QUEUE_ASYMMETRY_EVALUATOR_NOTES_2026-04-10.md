# Queue Asymmetry Evaluator Notes — 2026-04-10

## Purpose
Document the first real separation between:
- queue membership as static trigger list
- queue survival/removal as governance reasoning

This is not final canonical asymmetry intelligence.
It is the first explicit evaluator path that can be iterated without contaminating reporting or orchestration logic.

## Current Rule Hierarchy
1. **SENTINEL hard failure wins**
   - rejected / retired thesis -> remove
   - explicit unconfirmed thesis -> remove
2. **Active CDM/TDC pressure downgrades to monitor**
   - legal/regulatory/thesis pressure -> monitor instead of blind queue retention
3. **RISK_ON eval-only policy wins for designated names**
4. **Consensus-vs-asymmetry evaluator decides keep/remove/hold when no harder signal exists**
5. **If none of the above fires, regime posture remains transitional keep/watch/locked**

## What the first evaluator currently knows
### It can classify
- `GOOGL` as asymmetry retained / pre-consensus candidate
- `GEV`, `CEG`, `VST` as consensus-priced removal candidates
- `VRT` as hold-current-weight rather than size-up
- `BE` as SENTINEL-unconfirmed removal
- `NVDA` as RISK_ON eval-only

### It also uses
- live thesis status when available
- Gate 3 score threshold awareness
- CDM propagated pressure as a monitor downgrade path

## What it does NOT yet know
1. true valuation compression logic
2. dynamic consensus detection from market/news state
3. full Gate 3 re-evaluation from live evidence
4. distinction between good company and good queue candidate beyond current rules
5. time-horizon mismatch logic for monitor-list names

## Why this matters
Before this change, queue reasoning was effectively fused to presentation assumptions.
Now queue reasoning has its own layer:
- `src/execution/queue_reasoning.py`

That means future upgrades can focus on actual intelligence improvement instead of report patching.

## Next upgrades required
1. feed real TDC outcomes into queue reasoning
2. add valuation/compression-aware monitor transitions
3. add proper pre-consensus vs consensus scoring instead of ticker-specific rule hints
4. persist queue reasoning state for auditability
