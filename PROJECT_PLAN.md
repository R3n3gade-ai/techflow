# Achelion ARMS - Master Build Plan

This document outlines the development and implementation plan for the Achelion Risk Management System (ARMS), based on the Full-System Design (FSD) v1.1.

## Phase 1: Tier 0 Autonomy & Immediate-Build Frontiers (Months 1-2)

**Goal:** Achieve Tier 0 execution autonomy, replace subjective conviction with the MICS formula, and establish the core data and intelligence architecture. By the end of this phase, ARMS begins flying itself.

### Week 1: Setup & Core Logic

-   [ ] **Infrastructure Setup (AWS "The Fortress"):**
    -   [ ] Define Infrastructure as Code (IaC) using Terraform or CloudFormation.
    -   [ ] Provision core AWS services: VPC, ECS/Fargate for container orchestration, and RDS for PostgreSQL.
    -   [ ] Set up an in-memory cache using ElastiCache for Redis.
    -   [ ] Configure a task scheduling service (Prefect or Celery on ECS).
    -   [ ] Establish secure IAM roles, permissions, and secret management for API keys.
    -   [ ] Establish a secure connection endpoint for the IBKR paper trading account.
-   [ ] **Priority 1: Model-Implied Conviction Score (MICS)**
    -   [ ] Create `src/engine/mics.py`.
    -   [ ] Implement the MICS formula as specified in FSD Section 11.1.
    -   [ ] Define the data structures for SENTINEL gate inputs.
    -   [ ] Create a script to retroactively score the current Architecture AB portfolio and flag divergences for GP review.
-   [ ] **Priority 2: Foundational Code & Interfaces**
    -   [ ] Define and freeze the `OrderRequest` interface in `src/execution/interfaces.py`.
    -   [ ] Create the immutable session log structure and `audit_log.py` module for structured logging.

### Week 2-3: Data & Intelligence Foundations

-   [ ] **Priority 3: Feed-Agnostic Data Ingestion Pipeline**
    -   [ ] Define the `FeedPlugin` interface.
    -   [ ] Implement plugins for all specified free feeds (SEC EDGAR, FRED, USPTO, etc.).
-   [ ] **Priority 4: Session Log Analytics (SLA)**
    -   [ ] Create `src/engine/session_log_analytics.py`.
    -   [ ] Implement the three core learning loop metrics: CDF accuracy, regime transition lag, and SENTINEL Gate 3 accuracy.
-   [ ] **Priority 5: Information-Quality Confirmation Queue**
    -   [ ] Build `src/execution/confirmation_queue.py`.
    -   [ ] Implement the three-option response interface (Execute, Hold, Veto) as the primary interaction model.

### Week 4-6: Execution & Automation

-   [ ] **Priority 6: Brokerage API Integration**
    -   [ ] Build `src/execution/broker_api.py` as the sole interface to IBKR.
    -   [ ] Implement connection, position snapshot, order submission, and fill confirmation logic.
-   [ ] **Priority 7: Systematic Scan Engine**
    -   [ ] Build `src/engine/systematic_scan.py`.
    -   [ ] Integrate with Claude API wrapper for automated SENTINEL Gate 1 & 2 analysis.
    -   [ ] Schedule to run weekly via Prefect.
-   [ ] **Priority 8: Regime Probability Engine (RPE)**
    -   [ ] Build `src/engine/regime_probability.py`.
    -   [ ] Integrate with the data ingestion pipeline to provide continuous regime transition probabilities.

### Week 7-8: Integration & Testing

-   [ ] **Full Pipeline Integration:** Connect all Phase 1 modules.
-   [ ] **Paper Trading Validation:** Run the full system against the IBKR paper account for 30 days to validate all Tier 0 executions and monitoring.
-   [ ] **Daily Monitor v1:** Implement the initial version of the daily monitor, incorporating outputs from all new modules. Use the images in `monitor_examples/` as the definitive visual spec.

---

## Phase 2: Anticipatory Intelligence & Full Autonomy (Months 3-4)

*(Tasks to be detailed upon completion of Phase 1)*

## Phase 3: Licensable Platform & Self-Improvement (Months 5-6)

*(Tasks to be detailed upon completion of Phase 2)*
