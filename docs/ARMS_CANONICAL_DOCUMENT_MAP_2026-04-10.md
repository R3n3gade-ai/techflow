# ARMS Canonical Document Map — 2026-04-10

## Purpose
This document classifies the repository documentation into:
1. **Canonical architecture documents** — authoritative
2. **Supporting explanatory documents** — useful, subordinate to canonical docs
3. **Historical implementation / audit documents** — non-authoritative for present runtime truth
4. **Docs requiring cleanup / deprecation labeling**

The goal is to stop stale or optimistic implementation notes from outranking MJ's architecture.

---

## Tier 1 — Canonical Architecture Documents (Authoritative)
These define intended logic, math, operating behavior, execution philosophy, and module contracts.

### Core architecture
- `docs/ARMS_FSD_Master_Build_Document_v1.1.md`
- `docs/arms_technical_handoff_brief_v4.0.md`
- `docs/ARMS_v4.0_Briefing_Institutional_Risk_Management_and_Execution_Autonomy.md`

### Addenda / module specifications
- `docs/Addendum_1_ARMS_Module_Spec_PTRH_DSHP_v1.0.md`
- `docs/Addendum_2_ARMS_Module_Spec_CDM_TDC_v1.0.md`
- `docs/Addendum_3_ARMS_Intelligence_Architecture_Phase2_3_v1.0.md`
- `docs/arms_addendum_4_cam.md`
- `docs/ARMS_ADDENDUM_006.md`

### Infrastructure / operating environment
- `docs/ARMS_Infrastructure_Specification_v1.0.md`
- `docs/arms_infrastructure_specification.md` *(duplicate naming variant; keep one canonical path later)*
- `docs/INSTITUTIONAL_TECH_STACK_v2.0.md`
- `docs/DATA_FEED_MATRIX_v2.0.md`

### Backtesting / model spec (if still part of canonical 12)
- `docs/ARMS_BACKTESTING_ENGINE_SPEC.md`
- `docs/BACKTESTER_V2_SPEC.md` *(requires reconciliation / dedupe)*

---

## Tier 2 — Supporting / Explanatory Documents (Useful but Subordinate)
These help explain or communicate the architecture but should not override Tier 1.

- `docs/understanding_arms_gp_briefing.md`
- `docs/understanding_arms_gp_briefing_updated.md`
- `docs/ARMS_GP_Briefing_v1.0.md`
- `docs/ARMS_Plain_English_Executive_Summary.md`
- `docs/ARMS_Flight_Manual_Simple_Guide.md`
- `docs/ARMS_EOD_Snapshot_Spec_v1.0.md`
- `docs/DAILY_MONITOR_LAYOUT_REDESIGN_SPEC.md`
- `docs/daily_report_sample_layout_2026-04-01.md`

These are valuable, but if they contradict the FSD / THB / Addenda, the canonical docs win.

---

## Tier 3 — Historical Implementation / Progress Docs (Not Runtime Truth)
These document engineering work, but should be treated as logs, not as current truth.

- `docs/EXECUTION_HARDENING_SPRINT_1.md`
- `docs/EXECUTION_HARDENING_SPRINT_1_COMPLETE.md`
- `docs/EXECUTION_HARDENING_SPRINT_2.md`
- `docs/EXECUTION_HARDENING_SPRINT_2_COMPLETE.md`
- `docs/EXECUTION_HARDENING_SPRINT_3_COMPLETE.md`
- `docs/EXECUTION_HARDENING_SPRINT_4_COMPLETE.md`
- `docs/PTRH_ADDENDUM_6_IMPLEMENTATION.md`
- `docs/PTRH_ADDENDUM_6_IMPLEMENTATION_COMPLETE.md`
- `docs/DAILY_MONITOR_REDESIGN_IMPLEMENTATION.md`
- `docs/DAILY_MONITOR_REDESIGN_IMPLEMENTATION_COMPLETE.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_CORE_REBUILT.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_DAILY_MONITOR.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_DATA_PIPELINES.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_INTELLIGENCE.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_FINAL_AUDIT.md`
- `docs/ARMS_IMPLEMENTATION_STATUS_NEXT_STEPS.md`
- `docs/ARMS_ENGINEERING_STATUS_2026-04-07.md`
- `docs/ARMS_COMPREHENSIVE_CHECKPOINT_AUDIT_2026-04-08.md`
- `docs/ARMS_ENGINEERING_AUDIT_v2_APRIL_06.md`
- `docs/ARMS_ENGINEERING_AUDIT_v3_FULL_RECONCILIATION.md`
- `docs/ARMS_ENGINEERING_AUDIT_v4_FILE_TREE.md`
- `docs/ARMS_INSTITUTIONAL_ENGINEERING_AUDIT_v1.md`
- `docs/ARMS_LIVE_INTEGRITY_AUDIT_2026-04-07.md`
- `docs/ARMS_SPEC_ALIGNMENT_GAP_MAP_2026-04-07.md`

These may contain useful engineering detail, but they are not authoritative evidence that runtime parity has been achieved.

---

## Tier 4 — Duplicates / Cleanup Targets
These should be reconciled or explicitly deprecated to reduce confusion.

### Duplicate naming variants
- `docs/ARMS_FSD_Master_Build_Document_v1.1.md`
- `docs/arms_fsd_master_build_v1.1.md`

- `docs/ARMS_Infrastructure_Specification_v1.0.md`
- `docs/arms_infrastructure_specification.md`

- `docs/Addendum_2_ARMS_Module_Spec_CDM_TDC_v1.0.md`
- `docs/arms_addendum_2_cdm_tdc.md`

- `docs/Addendum_1_ARMS_Module_Spec_PTRH_DSHP_v1.0.md`
- `docs/arms_addendum_ptrh_dshp.md`

### Overlapping partner / explanatory docs
- `docs/understanding_arms_gp_briefing.md`
- `docs/understanding_arms_gp_briefing_updated.md`
- `docs/ARMS_GP_Briefing_v1.0.md`

### Backtest spec overlap
- `docs/ARMS_BACKTESTING_ENGINE_SPEC.md`
- `docs/BACKTESTER_V2_SPEC.md`

---

## Documentation Rules Going Forward
1. Tier 1 always wins.
2. Tier 3 docs must never be treated as proof of current runtime readiness.
3. Any doc that makes completion claims must state whether it is:
   - architectural target
   - historical implementation note
   - current runtime truth
4. Duplicate naming variants should be collapsed or labeled clearly.
5. New engineering truth should be recorded in runtime-truth docs, not in completion-flavored status notes.

---

## Immediate Cleanup Actions
1. Add "historical / not authoritative runtime truth" banner to Tier 3 docs that overstate completion.
2. Reconcile duplicate canonical docs into one preferred path each.
3. Use `ARMS_RUNTIME_TRUTH_AUDIT_2026-04-10.md` as the cold-truth reference for current state.
