# Execution Hardening Sprint 1

## Objective
Make ARMS capable of a trustworthy paper-trading execution loop built on a single canonical execution contract.

## Sprint Priorities

### 1. Contract Unification
- Select one canonical `OrderRequest`
- Remove duplicate/conflicting definitions
- Refactor all trade-producing modules to use the same contract
- Define lifecycle states and required fields by order type / tier

### 2. IBKR Paper Adapter Foundation
- Connect to IB Gateway / TWS (paper)
- Retrieve account + positions
- Submit simple equity paper orders
- Retrieve status/fill information
- Introduce error handling and reconnect scaffolding

### 3. Durable Control Plane Design
- Replace placeholder queue objects
- Persist pending confirmations
- Tie approvals/vetoes to canonical request IDs
- Prepare timeout execution path

### 4. Verification
- Repair stale tests
- Add minimal contract validation tests
- Add broker adapter smoke tests
- Add signal->order->audit integration checks

## Deliverables
- canonical execution contract
- refactored module imports/callsites
- initial IBKR paper adapter
- queue persistence design / scaffold
- repaired baseline test layer

## Non-Goals for Sprint 1
- live-money deployment
- full PDF monitor redesign
- complete alt-data rollout
- institutional-grade infra migration

## Exit Criteria
- one canonical order schema in repo
- no placeholder order object in active path
- paper broker connection works
- paper positions can be read
- at least one safe paper test order can be submitted and traced
- audit trail ties request ID -> broker action
