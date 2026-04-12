> **? STALE DOCUMENT — NOT AUTHORITATIVE**
> This document predates significant code changes (April 2026 remediation cycle).
> For current system truth, see: ARMS_NEXT_WAVE_COLD_TRUTH_AUDIT_2026-04-10.md
> and ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md

# Execution Hardening Sprint 2: Control Plane

## Objective
Build a durable, restart-safe governance layer (Tier 1 & Tier 2 Confirmation Queue) and establish a complete end-to-end correlation ID chain from signal generation to broker execution and audit logging.

## Priorities
### 1. Persistent Confirmation Queue
- Replace in-memory list in `ConfirmationQueue` with a durable storage backend (JSON or SQLite).
- Ensure pending actions survive system restarts.
- Add timeout tracking (auto-execution on timeout for Tier 1 default-execute items).

### 2. Execution Correlation IDs
- Assign a unique, immutable UUID or correlation ID to every `OrderRequest`.
- Ensure the correlation ID is logged in the `SessionLog` at creation, approval, and execution.
- Map the internal correlation ID to the broker's `orderId` in the adapter.

### 3. Queue Governance Interface
- Separate "PENDING" items into Tier 1 (Veto Window) and Tier 2 (PM Confirm Required).
- Support explicit source declarations (Cat A, Cat B) upon Tier 1/Tier 2 confirmation.

### 4. Position Reconciliation Scaffold
- Update the Master Engine to read actual portfolio positions from the broker adapter instead of using mocked state.

## Exit Criteria
- Confirmation queue restarts with pending actions intact.
- An order can be traced via correlation ID from `CDP_TRIGGER` -> `QUEUE_PENDING` -> `QUEUE_APPROVED` -> `BROKER_SUBMIT` -> `BROKER_FILLED`.
- Master Engine pulls live positions.
