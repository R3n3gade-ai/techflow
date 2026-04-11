# ARMS Remediation Master Plan — 2026-04-10

## Mission
Restore strict runtime alignment between the codebase and MJ's canonical ARMS architecture so that:
- live inputs are real and typed
- deterministic decisions are system-owned
- queue logic matches canonical asymmetry / governance rules
- execution semantics are institution-grade
- the Daily Monitor emerges correctly from system truth instead of presentation compensation

This plan is ordered intentionally. Do not start with cosmetic report fixes.

---

## North Star
When this plan is complete:
1. the live cycle runs without synthetic critical inputs
2. queue membership is derived from canonical logic, not static lists
3. SENTINEL / TDC / CDM materially influence state
4. Daily Monitor is a pure rendering of system truth
5. runtime behavior can be defended against MJ's docs line by line

---

## Workstream 1 — Documentation Cleanup and Truth Control
### Goal
Stop outdated or optimistic docs from confusing engineering direction.

### Tasks
1. label implementation-status and sprint docs as historical/non-authoritative
2. identify preferred canonical path for duplicate doc pairs
3. maintain one current runtime-truth audit doc
4. create a "canonical 12" index if needed from the user's preferred set

### Exit criteria
- engineers cannot accidentally use stale implementation notes as runtime truth

---

## Workstream 2 — L1 Data Integrity Hardening
### Goal
Eliminate silent synthetic inputs and incomplete critical feeds in live mode.

### Tasks
1. remove production-mode fallback value insertion from `fred_plugin.py`
2. define approved secondary deterministic sources for critical macro inputs (if any)
3. make PMI mandatory for live regime operation or provide an approved live fallback source
4. classify each current bridge file as either:
   - acceptable transitional typed state
   - must be replaced by autonomous live derivation
5. make missing critical inputs fail loud with clear diagnostics

### Exit criteria
- no live regime calculation depends on silent synthetic defaults
- all critical L1 inputs have explicit provenance

---

## Workstream 3 — Typed Event / Catalyst State Layer
### Goal
Turn event/news flow into structured state consumed by ARAS, queue governance, and reporting.

### Tasks
1. design a typed event-state model for:
   - diplomacy / negotiation state
   - oil / Hormuz disruption state
   - legal / regulatory shock state
   - named catalyst calendar
   - event severity / freshness
2. route `news_rss_feed`, SEC, and manual event bridge into that typed model
3. remove hidden "LLM event overlay" as the primary regime-event integration path
4. expose typed event state to L2, L3, and L7

### Exit criteria
- event information influences the system through typed state, not only prompt prose

---

## Workstream 4 — Queue Intelligence Engine
### Goal
Replace simple threshold queueing with canonical institutional queue governance.

### Tasks
1. redesign `strategic_queue.py` into a true queue intelligence module
2. encode states such as:
   - LOCKED
   - WATCH
   - TRIGGERED
   - EVAL_ONLY
   - HOLD_CURRENT_WEIGHT
   - REMOVED
   - MONITOR_LIST
3. encode reason classes such as:
   - consensus-priced
   - asymmetry retained
   - SENTINEL unconfirmed
   - time-horizon mismatch
   - valuation compression required
4. wire queue reevaluation to:
   - SENTINEL state
   - TDC state
   - event-state layer
   - regime state
5. support NEUTRAL trigger and RISK_ON eval distinctions per canonical docs

### Exit criteria
- queue output structurally explains why each name survives, holds, moves to monitor, or is removed

---

## Workstream 5 — SENTINEL / CDM / TDC Integration
### Goal
Make thesis truth operational, not isolated.

### Tasks
1. make `sentinel_workflow.py` the single source of thesis state
2. rework `tdc.py` to consume real thesis records instead of placeholder gate context
3. persist thesis-integrity changes in a form consumable by queue and monitor
4. connect CDM propagation directly into thesis re-evaluation and queue status
5. map outcomes to monitor/report statuses (OK / WATCH / THESIS+ / TRIMMED / HOLD / REMOVED)

### Exit criteria
- thesis state actively governs deployment state and monitor output

---

## Workstream 6 — Daily Monitor State Rebuild
### Goal
Make the monitor a renderer of full institutional state.

### Tasks
1. define a typed `DailyMonitorState` / equivalent that includes:
   - weekly scorecard
   - current regime / prior regime / direction
   - catalyst schedule
   - macro input cards
   - queue state
   - monitor list
   - removed queue items with reasons
   - equity book with real statuses and performance windows
   - defensive sleeve state
   - module panels
   - PM decision queue
2. eliminate placeholder report fields from `main.py`
3. restrict LLM use to prose synthesis where structured state already exists
4. ensure renderer does not fabricate logic the system did not compute

### Exit criteria
- if the system state is right, the report is right
- if the system state is wrong, the report reveals that honestly

---

## Workstream 7 — Execution Hardening
### Goal
Bring broker and order semantics to institutional readiness.

### Tasks
1. remove ugly emergency defaults from `broker_api.py`
2. formalize price-source policy for:
   - live market price
   - delayed market price
   - close fallback
   - reject execution
3. implement stricter order eligibility validation
4. improve options chain / Greeks sourcing for PTRH
5. add stronger order status / fill reconciliation / submission audit
6. ensure no real-money path depends on ad hoc arithmetic shortcuts

### Exit criteria
- execution path is explicit, deterministic, and auditable

---

## Workstream 8 — Runtime Validation Harness
### Goal
Prevent drift from reappearing.

### Tasks
1. define expected-output checks for live cycle state objects
2. add regression checks for:
   - regime computation integrity
   - queue reasoning integrity
   - monitor state completeness
   - broker submission semantics
3. compare generated monitor state against canonical architecture expectations after each major fix

### Exit criteria
- future regressions surface immediately instead of via painful report mismatch

---

## Recommended Execution Order
1. Documentation cleanup / truth control
2. L1 data integrity hardening
3. Typed event-state layer
4. Queue intelligence engine
5. SENTINEL / TDC / CDM integration
6. Daily Monitor state rebuild
7. Execution hardening
8. Regression harness and final validation

---

## Definition of Done
ARMS is not "done" when it looks polished.
ARMS is done when:
- all critical live inputs are sourced truthfully
- queue logic matches canonical governance rules
- risk and thesis layers control state correctly
- execution behavior is institution-grade
- the Daily Monitor is a faithful consequence of runtime truth
- discrepancies against MJ docs can be explained by market reality, not architectural gaps

---

## Immediate Next Step
Begin with:
1. documentation truth cleanup
2. removal of synthetic critical feed fallbacks
3. design of typed queue / monitor state contracts

No more report-first fixes.
System truth first.
