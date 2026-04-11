# NEXT DEV HANDOFF — 2026-04-10

## Read this first
If you are picking up ARMS after the current remediation wave, do **not** start from the old implementation-status docs or completion claims.
Start here, in order:

1. `docs/ARMS_RUNTIME_TRUTH_AUDIT_2026-04-10.md`
2. `docs/ARMS_NEXT_WAVE_COLD_TRUTH_AUDIT_2026-04-10.md`
3. `docs/ARMS_CANONICAL_DOCUMENT_MAP_2026-04-10.md`
4. `docs/ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md`
5. MJ canonical docs (FSD / THB / Addenda)

## What just got fixed in this remediation wave
### Truth/documentation cleanup
- historical/non-authoritative banners added to multiple misleading status docs
- new runtime-truth audit docs created
- canonical document map created
- remediation master plan created

### Data integrity
- strict live feed mode enforced for FRED/PMI path
- silent synthetic macro fallback behavior removed in strict mode

### Queue / governance architecture
- typed monitor state created
- typed queue governance state created
- queue reasoning layer created
- durable TDC state created and wired into queue reasoning
- queue reasoning upgraded to include asymmetry/consensus transitional evaluator
- removed/downgraded/monitor list now flow into Daily Monitor markdown path

### TDC
- TDC no longer reviews against placeholder thesis blob
- TDC now uses stored SENTINEL thesis record
- TDC writes durable state consumed by queue reasoning

### Broker hardening
- removed fake connected-mode fallback from `broker_api.py`
- removed arbitrary notional conversion fallback arithmetic
- implemented real order-status mapping foundation

### Macro Compass
- removed opaque LLM event-overlay from live regime path
- replaced with deterministic typed macro event-state derivation

## What is still broken / incomplete
### Highest priority remaining
1. `src/execution/broker_api.py`
   - options path still needs more hardening
   - order reconciliation still thin
   - formal price policy doc still needed
2. `src/main.py`
   - still contains transitional report scaffolding (`Next Catalyst`, fixed prior score, generic decision queue, zero session perf)
3. `src/reporting/daily_monitor_view.py`
   - stale mock-oriented HTML path still exists and is dangerous if mistaken for truth
4. queue reasoning still contains transitional heuristics for consensus/asymmetry
5. TDC weekly audit still stubbed
6. queue transitions not yet persisted as first-class audit state

## Non-negotiable project rule
Do not patch outputs to match MJ manually.
If output is wrong, fix the system state path that generated it.

## Immediate next recommended tasks
1. finish `broker_api.py` hardening for options + reconciliation
2. remove or deprecate stale HTML/mock monitor path
3. replace `main.py` report scaffolding with real derived fields
4. persist queue state transitions
5. build richer event-state/catalyst model
6. implement weekly TDC audit

## Architectural principle to preserve
ARMS is a typed seven-layer institutional pipeline.
Not a bundle of scripts.
Not an LLM report generator.
Not a narrative patch engine.

The report is the consequence of system truth.
If the report is wrong, the architecture upstream is wrong.
