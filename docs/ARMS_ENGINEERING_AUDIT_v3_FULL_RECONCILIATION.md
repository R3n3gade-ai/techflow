# Achelion ARMS Engineering Audit v3 (Full Document Reconciliation)

This is a comprehensive audit comparing the stated architecture across the 12 canonical documents in the workspace against the actual physical files present in the `achelion_arms` repository.

## 1. The Good News: What is Perfectly Aligned
The new modules built in Sprints 1-3 perfectly match the specifications in the addenda:
- **Addendum 6 (PTRH Adaptive Strike):** The Delta-primary (-0.35) option scanning logic is built and physically integrated into `src/engine/tail_hedge.py` and `broker_api.py`.
- **Addendum 1 (PTRH/DSHP):** Gain harvesting rules for SGOL (20%) and DBMF (15%) are physically implemented in `src/engine/dshp.py`.
- **Addendum 2 (CDM/TDC):** The event propagation logic (Customer Dependency Map) and AI thesis checking prompt structure are physically implemented in `src/engine/cdm.py` and `src/engine/tdc.py`.
- **FSD v1.1 (MICS/SLA/Queue):** The Model-Implied Conviction Score math is physically implemented in `src/engine/mics.py`. The persistent confirmation queue is physically implemented in `src/execution/confirmation_queue.py`.

## 2. The Critical Gap: Missing Legacy Core Files
The `docs/arms_technical_handoff_brief_v4.0.md` (THB) and `docs/CODEBASE_GAME_PLAN_v2.0.md` both explicitly state that the **Phase 0 Foundation** was completed and the core v3.1 logic was migrated.

**CODEBASE_GAME_PLAN_v2.0.md (Step 1):**
> - **Kevlar Limits:** Hard limits enforced (22% max single position, 3% minimum, 48% total AI sector cap).
> - **ARAS Logic:** `aras.py` (legacy) logic migrated to `src/engine/` with CORRELATED stress source detection.

**arms_technical_handoff_brief_v4.0.md (Section 10):**
> `src/engine/aras.py` # unchanged core
> `src/engine/macro_compass.py` # unchanged
> `src/engine/master_engine.py` # updated
> `src/engine/kevlar.py` # unchanged

### The Reality in the Codebase
**None of these files exist in the `src/engine/` directory.** 

If you run `ls src/engine/` in the terminal, you will only see the new modules (MICS, CAM, PTRH, DSHP, CDM, TDC, RPE, ARES, CDF, CCM, TRP, AUP, Incapacitation). 

There is no `aras.py`. There is no `macro_compass.py`. There is no `master_engine.py`. There is no `kevlar.py`. 

### The Operational Impact
Because these files are missing:
1. `src/main.py` is forced to hardcode the regime: `current_regime="WATCH", regime_score=0.35` because it has no `macro_compass.py` to calculate it.
2. The portfolio has no way to calculate actual target allocation weights because `master_engine.py` (which takes the MICS score and translates it into a percentage) is missing.
3. The system cannot enforce the 22% single-position limit because `kevlar.py` is missing.

## 3. Recommendation
This happens frequently during handoffs when a developer builds new modules (Phase 1/2) in a fresh repository but forgets to copy over the legacy core files from the old v3.1 repository.

**We have two options:**
1. **Find the old files:** If MJ or Josh have the original `aras.py`, `macro_compass.py`, and `master_engine.py` files from the v3.1 repository, paste them into the workspace and I will integrate them immediately.
2. **Rebuild them from the specs:** The FSD and THB are so detailed that I can rewrite the ARAS regime logic, the Macro Compass, and the Master Engine from scratch based purely on the math described in the documents.

This is the exact reason we run these audits. The new nervous system is flawless, but the brain stem was left behind in the old repo.