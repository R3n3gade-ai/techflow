# ARMS Runtime Truth Audit — 2026-04-10

## Status
**COLD TRUTH / RESET AUDIT**

This document supersedes any optimistic or completion-framed status narrative when evaluating actual runtime readiness.
It is the working truth document for bringing ARMS back into strict alignment with MJ's canonical architecture.

## Governing Standard
The only authoritative standard for ARMS behavior is the canonical MJ document set:
- `docs/ARMS_FSD_Master_Build_Document_v1.1.md`
- `docs/arms_technical_handoff_brief_v4.0.md`
- `docs/ARMS_v4.0_Briefing_Institutional_Risk_Management_and_Execution_Autonomy.md`
- `docs/Addendum_1_ARMS_Module_Spec_PTRH_DSHP_v1.0.md`
- `docs/Addendum_2_ARMS_Module_Spec_CDM_TDC_v1.0.md`
- `docs/Addendum_3_ARMS_Intelligence_Architecture_Phase2_3_v1.0.md`
- `docs/arms_addendum_4_cam.md`
- `docs/ARMS_ADDENDUM_006.md`
- plus the remaining partner-facing / explanatory master documents that describe architecture intent, operating philosophy, infrastructure, and reporting behavior.

If code, reports, bridge files, fallback behavior, or internal status docs contradict the above, the MJ docs win.

---

## Executive Summary
ARMS currently contains a meaningful amount of real infrastructure and real logic:
- live IBKR paper connectivity is working
- live NAV / positions can be pulled
- real order submission is functioning
- major risk modules exist in code
- the orchestrator can complete an end-to-end sweep

However, ARMS is **not yet institutionally faithful to the canonical architecture at runtime**.

The largest gap is not one single bug. The gap is that the system still runs in a mixed state composed of:
1. **real live components**
2. **bridge-backed interim components**
3. **presentation-layer scaffolding**
4. **optimistic status documentation that overstates completion**

That mixed state is what caused the April 10 Daily Monitor drift from MJ's real operating output.

The Daily Monitor is currently exposing the underlying architectural integrity problem. The monitor is not the core failure by itself; it is the visible symptom of deeper state, data, and control-path inconsistencies.

---

## What the Canonical Documents Require
From the FSD and v4.0 architecture:
- ARMS must function as a **typed seven-layer pipeline**, not a loose script bundle.
- The PM declares intent; ARMS executes everything else.
- Human involvement at the execution layer is latency / error risk, not safety.
- Regime, sizing, queue logic, hedge state, and reporting must be derived from sourced system state.
- The Daily Monitor is an output artifact of real system state, not a compensating narrative layer.
- Any deterministic operation that still depends on human confirmation is evidence of incomplete build.

---

## Runtime Findings by Layer

### L1 — Data Ingestion
**Current reality:** partially live, partially brittle, partially fallback-backed.

Observed issues:
- `fred_plugin.py` still inserts fallback macro values when FRED fails.
- PMI ingestion is optional based on env wiring instead of being guaranteed for live regime computation.
- public RSS news is fetched but not transformed into a robust typed state model consumed consistently downstream.
- some bridge/state files remain missing during live sweep (`rss_inputs`, `cdf_inputs`, `macro_event_overlay`, etc.).

Why this violates spec:
- Critical regime inputs should not silently degrade into synthetic placeholders in a live cycle.
- The architecture requires sourced, typed outputs into L2, not partial live data plus convenience fallback values.

**Audit conclusion:** L1 is not yet institutionally trustworthy.

---

### L2 — Macro Compass / ARAS
**Current reality:** core scoring exists, but the event and qualitative integration path is not yet canonical.

Observed issues:
- `macro_compass.py` computes a score from VIX / HY / PMI / 10Y, which is directionally correct.
- event stress currently relies on an LLM inference overlay path rather than a disciplined, typed event-state framework.
- the engine is not clearly producing the same catalyst-aware, institutionally explainable state reflected in MJ's monitor.

Why this violates spec:
- Regime state must be auditable and reproducible.
- Qualitative event influence should not be smuggled in through opaque LLM overlay behavior.
- The live system should explain *why* score stabilized at e.g. ~0.73 using structured event inputs, not prompt magic.

**Audit conclusion:** L2 exists, but is not yet canonical-grade.

---

### L3 — Risk / Governance / Intelligence Modules
**Current reality:** many modules exist, but several are not fully integrated into the live decision graph.

#### SENTINEL
- `sentinel_workflow.py` is promising and durable.
- But its outputs are not yet fully wired into queue maintenance, monitor state, and downstream portfolio governance.

#### TDC
- `tdc.py` still contains placeholder characteristics, including hardcoded / simplified source context paths.
- It is not clearly consuming the live SENTINEL record as the single source of thesis truth.

#### CDM
- dependency mapping exists conceptually and in config.
- but live propagation into queue posture, monitor flags, and thesis-state transitions remains incomplete.

#### PTRH / CAM
- live options chain requests exist.
- Addendum 6 delta-primary intent is partially implemented.
- but live chain / Greeks sourcing is still not robust enough, and broker/data subscription realities are still bleeding into execution quality.

#### CDF / RSS / bridge-backed analytics
- some former hardcoded values have been moved into bridge/state files, which is better than hardcoding.
- but bridge-backed interim state is still not the same thing as fully autonomous live derivation.

Why this violates spec:
- MJ's docs require deterministic, autonomous governance logic wherever the answer can be derived from math / data / process.
- If queue membership, thesis validity, or monitor flags are not continuously derived from live system state, ARMS is still incomplete.

**Audit conclusion:** L3 has meaningful implementation, but integration depth is insufficient.

---

### L4 / L5 — Master Engine / Order Book / Queue Control
**Current reality:** real rebalancing and broker dispatch exist, but queue intelligence is underdeveloped.

Observed issues:
- `strategic_queue.py` is a simple trigger list, not a true institutional deployment-governance engine.
- it does not encode:
  - removal reasons
  - monitor-list migration
  - consensus-pricing invalidation
  - SENTINEL revalidation failure
  - RISK_ON eval-only behavior with proper governance semantics
- `main.py` currently assembles important state manually rather than consuming a rich typed queue/governance output.

Why this violates spec:
- MJ's architecture requires system-driven queue discipline.
- The system should autonomously know why a name is in queue, out of queue, on monitor, or eval-only.
- The monitor discrepancy around GOOGL vs GEV/CEG/VST/VRT is direct evidence this layer is incomplete.

**Audit conclusion:** L4/L5 execution exists; L4/L5 governance fidelity does not.

---

### L6 — Broker / Execution API
**Current reality:** live paper connectivity is real, but code cleanliness and execution-policy integrity are not yet institutional.

Observed issues:
- broker connection is live and orders can hit IBKR paper.
- but `broker_api.py` still contains emergency fallback behavior and ugly price-conversion logic.
- delayed/live price handling remains insufficiently formalized.
- options execution path remains underhardened.
- order status / reconciliation / fill lifecycle are incomplete.

Why this violates spec:
- half a billion dollars cannot run on ad hoc fallback arithmetic.
- execution semantics must be explicit, deterministic, and auditable.

**Audit conclusion:** live connectivity achieved; institutional execution hardening incomplete.

---

### L7 — Daily Monitor / Audit / Reporting
**Current reality:** polished rendering exists, but the state object feeding it is underpowered and partially scaffolded.

Observed issues in `main.py` / `daily_monitor.py`:
- report inputs still contain hand-assembled values
- placeholders remain (`Next Catalyst`, generic driver strings, fixed yesterday score, zero session performance, empty deployment queue)
- LLM synthesis is being asked to compensate for missing structured truth
- renderer is doing more than rendering because the upstream state is too thin

Why this violates spec:
- the Daily Monitor should be the final expression of already-computed institutional truth
- if the upstream state is incomplete, the report will drift no matter how good the prose is

**Audit conclusion:** reporting quality exceeds reporting truth.

---

## Root Cause of the April 10 Report Discrepancy
The discrepancy with MJ's April 10 monitor was caused by **system-state incompleteness**, not by MJ "changing the story".

The main causes are:
1. **Queue intelligence not fully implemented**
   - the system cannot yet autonomously prune names based on consensus-pricing decay / asymmetry failure / SENTINEL non-confirmation
2. **Daily Monitor state object too thin**
   - missing weekly scorecard, monitor list, removed queue items, reason codes, catalyst calendar, queue governance detail
3. **L2 event integration not canonical**
   - event reality is not being transformed into typed regime / catalyst / narrative state cleanly enough
4. **Bridge and fallback contamination**
   - live cycle still tolerates too much degraded input in places that should fail loud or switch to approved secondary deterministic sources
5. **Outdated / optimistic internal docs obscuring actual readiness**
   - some audit/status documents overstate completion and therefore hide the real engineering backlog

---

## What Is Outdated or Dangerous in the Documentation Set
The following classes of docs should be treated as **historical progress notes**, not runtime truth:
- `docs/ARMS_COMPREHENSIVE_CHECKPOINT_AUDIT_2026-04-08.md`
- `docs/ARMS_ENGINEERING_STATUS_2026-04-07.md`
- any `IMPLEMENTATION_STATUS_*` or sprint-complete doc that claims full live alignment without caveat

These documents are not necessarily false in intent, but they are dangerous if used as present-tense runtime truth.

### Documentation policy going forward
Classify docs into three groups:
1. **Canonical MJ architecture** — always authoritative
2. **Historical implementation logs** — useful, but not authoritative
3. **Runtime truth docs** — current cold-truth engineering state

Only group (1) and current group (3) should drive remediation decisions.

---

## Recovery Plan

### Phase 1 — Truth and cleanup
1. Mark outdated implementation-status docs as historical / superseded where appropriate.
2. Build a canonical index of the main MJ document set and classify every other doc relative to it.
3. Remove or quarantine runtime scaffolds that encourage false confidence.

### Phase 2 — Fix the architecture in the right order
1. **Rebuild Daily Monitor as pure renderer**
   - no placeholder inputs
   - no thin state object
   - consume a typed institutional monitor state
2. **Implement Queue Intelligence properly**
   - queue membership
   - monitor list
   - removal reasons
   - SENTINEL/TDC integration
   - consensus-pricing invalidation
3. **Repair L1/L2 integrity**
   - remove silent FRED synthetic fallback in production mode
   - make PMI mandatory for live cycle or provide approved secondary deterministic source
   - replace LLM macro overlay shortcuts with typed event-state inputs
4. **Wire SENTINEL/CDM/TDC into queue and report state**
5. **Finish execution hardening**
   - market-price policy
   - order lifecycle reconciliation
   - options data / Greeks / chain quality
   - eliminate ugly emergency arithmetic fallbacks

### Phase 3 — Revalidate end-to-end
1. run live paper sweep
2. compare generated monitor against canonical expected architecture behavior
3. only when system state is natively correct should monitor parity be expected

---

## Non-Negotiable Rules From This Point Forward
1. Do not patch reports to match MJ manually.
2. Do not use LLM prose to hide missing structured system state.
3. Do not allow critical regime inputs to silently degrade into synthetic defaults in live mode.
4. Do not claim architectural completion unless runtime evidence supports it.
5. If the system does not know something natively, that is an engineering backlog item — not a narrative problem.

---

## Immediate Next Deliverables
1. `docs/ARMS_CANONICAL_DOCUMENT_MAP_2026-04-10.md`
2. `docs/ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md`
3. cleanup pass on outdated / overstated implementation docs
4. code remediation beginning with typed monitor state + queue intelligence

---

## Bottom Line
ARMS is not broken in the sense of being fake.
ARMS is broken in the more dangerous sense of being **partly real, partly interim, and partly overclaimed**.

That is why the output drifted.
That is the setback.
And that is what must be corrected systematically against MJ's canonical architecture.
