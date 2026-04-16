# Achelion ARMS — Codebase Map
**Last Updated: April 16, 2026**

```
techflow/
+-- .env                          # API keys (gitignored)
+-- .gitignore
+-- MASTER_IMPLEMENTATION_PLAN.md  # What is built vs pending
+-- CODEBASE_MAP.md                # This file
+--
+-- docs/
|   +-- ARMS_API_CONNECTIONS_REQUIRED.md   # Live connection checklist
|   +-- ARMS_FSD_Master_Build_Document_v1.1.md
|   +-- ARMS_GP_Briefing_v1.0.md
|   +-- ARMS_Infrastructure_Specification_v1.0.md
|   +-- (additional spec/audit documents)
+--
+-- infra/
|   +-- main.tf                    # Terraform: ECS/RDS/Redis/S3/SNS
|   +-- variables.tf
|   +-- outputs.tf
+--
+-- system_map/
|   +-- index.html                 # Interactive architecture visualization
+--
+-- src/
    +-- main.py                    # Full 7-phase ARMS orchestration cycle
    +-- run_daily_report.py        # Standalone daily report runner
    +--
    +-- data_feeds/                # L1 — Market Data Ingestion
    |   +-- pipeline.py            #   Orchestrates 4 production feed plugins
    |   +-- fred_plugin.py         #   FRED API (VIX, 10Y, HY, T10Y2Y, PCR, Margin Debt)
    |   +-- crypto_plugin.py       #   IBKR CME futures + Coinbase spot + CBOE SKEW
    |   +-- coinglass_feed.py      #   CoinGlass (funding, OI, liquidations, long/short, BTC price)
    |   +-- pmi_plugin.py          #   ISM Manufacturing PMI from CSV bridge
    |   +-- sec_edgar_feed.py      #   SEC EDGAR Form 4 insider trades
    |   +-- sec_edgar_plugin.py    #   SEC EDGAR (requests/BS4 variant)
    |   +-- news_rss_feed.py       #   Public RSS news ingestion
    |   +-- event_bridge.py        #   Manual event bridge (dev)
    |   +-- event_state.py         #   Event deduplication
    |   +-- macro_event_state.py   #   Typed macro event classification
    |   +-- interfaces.py          #   SignalRecord, FeedPlugin ABC
    |   +-- feed_interface.py      #   Alternate FeedPlugin ABC
    +--
    +-- engine/                    # L2-L4 — Core Risk & Conviction Engines
    |   +-- macro_compass.py       #   L2: Regime scoring (0.0-1.0)
    |   +-- aras.py                #   L3: ARAS regime -> ceiling + EDR advisory
    |   +-- master_engine.py       #   L4: Target weight construction
    |   +-- mics.py                #   MICS conviction scoring formula
    |   +-- kevlar.py              #   22% single-name concentration cap
    |   +-- drawdown_sentinel.py   #   PDS portfolio drawdown sentinel
    |   +-- factor_exposure.py     #   FEM 5-factor concentration check
    |   +-- cam.py                 #   CAM tail hedge sizing
    |   +-- tail_hedge.py          #   PTRH autonomous put rolling
    |   +-- dshp.py                #   DSHP defensive sleeve harvest
    |   +-- cdm.py                 #   CDM entity signal propagation
    |   +-- tdc.py                 #   TDC thesis integrity audit (LLM)
    |   +-- cdf.py                 #   CDF position decay (45/90/135d)
    |   +-- regime_probability.py  #   RPE regime transition forecast
    |   +-- ares.py                #   ARES re-entry system + VARES
    |   +-- mc_rss.py              #   MC-RSS retail sentiment
    |   +-- incapacitation.py      #   PM heartbeat safety backstop
    |   +-- asymmetric_upside.py   #   AUP stability unlocks
    |   +-- slof.py                #   SLOF leverage overlay
    |   +-- paie.py                #   PAIE pre-execution integrity
    |   +-- perm.py                #   PERM covered call automation
    |   +-- laep.py                #   LAEP 5-tier VIX execution
    |   +-- thesis_retirement.py   #   TRP orderly exit protocol
    |   +-- conviction_calibration.py  # CCM learning loop
    |   +-- systematic_scan.py     #   Weekly autonomous thesis scan (LLM)
    |   +-- session_log_analytics.py   # SLA monthly metrics
    |   +-- sentinel_workflow.py   #   SENTINEL thesis lifecycle
    |   +-- sentinel_bridge.py     #   Interim MICS gate data bridge
    |   +-- cdf_analytics.py       #   Live underperformance vs QQQ
    |   +-- cdf_bridge.py          #   Interim CDF input bridge
    |   +-- cdf_state.py           #   CDF state persistence
    |   +-- mc_rss_analytics.py    #   Live NAAIM scraping
    |   +-- rss_bridge.py          #   Interim RSS input bridge
    |   +-- bridge_health.py       #   Bridge file staleness check
    |   +-- bridge_paths.py        #   Bridge path resolution
    |   +-- pds_state.py           #   PDS high-water mark state
    |   +-- tdc_state.py           #   TDC TIS score persistence
    +--
    +-- intelligence/              # L6 — AI / LLM Intelligence Layer
    |   +-- llm_wrapper.py         #   Multi-provider LLM bridge
    |   +-- kb_ingest.py           #   Vector KB ingest pipeline
    |   +-- gate3_supplementary.py #   Gate 3 anticipatory scoring
    |   +-- elvt.py                #   Earnings language velocity
    |   +-- jpvi.py                #   Job posting velocity
    |   +-- pfvt.py                #   Patent filing velocity
    |   +-- sccr.py                #   Supply chain cross-reference
    +--
    +-- execution/                 # L5 — Order Execution & Safety
    |   +-- broker_api.py          #   IBKR ib_insync adapter
    |   +-- order_book.py          #   L5 order book + LAEP tiers
    |   +-- order_request.py       #   OrderRequest dataclass
    |   +-- trade_order_generator.py   # Weight -> OrderRequest diff
    |   +-- circuit_breaker.py     #   SPX -5% / VIX >30 kills
    |   +-- confirmation_queue.py  #   Tier 1/2 confirmation queue
    |   +-- strategic_queue.py     #   Regime-triggered deploy queue
    |   +-- correlation_monitor.py #   30d equity/crypto correlation
    |   +-- escalation_engine.py   #   Cumulative loss auto-suppress
    |   +-- overnight_monitor.py   #   ES/VIX futures gap monitor
    |   +-- pm_protocol.py         #   GP co-sign protocol
    |   +-- queue_state.py         #   Queue governance state machine
    |   +-- queue_reasoning.py     #   Queue signal aggregation
    |   +-- queue_persistence.py   #   Queue transition logging
    |   +-- interfaces.py          #   Position dataclass, Broker ABC
    +--
    +-- modules/                   # ARAS Sub-Modules
    |   +-- deleveraging_risk.py   #   Systemic deleveraging detection
    |   +-- margin_stress.py       #   Margin pressure (HY+VIX)
    |   +-- dealer_gamma.py        #   Dealer gamma positioning
    |   +-- crypto_microstructure.py   # Crypto market health
    |   +-- pcr_regime.py          #   Put/call ratio regime
    |   +-- shutdown_risk.py       #   Macro event calendar
    |   +-- stress_scenarios.py    #   Historical stress scenarios
    +--
    +-- reporting/                 # L7 — Reporting & Diagnostics
    |   +-- daily_monitor.py       #   Daily Monitor v4.0 (LLM)
    |   +-- eod_snapshot.py        #   EOD 5-field closing check
    |   +-- proactive_digest.py    #   Monthly LP digest (LLM)
    |   +-- performance_attribution.py # Module alpha attribution
    |   +-- audit_log.py           #   Immutable JSONL session log
    |   +-- monitor_state.py       #   Monitor state types
    |   +-- regime_history.py      #   Regime transition history
    |   +-- report_context.py      #   Report context aggregation
    +--
    +-- scheduling/                # Job Scheduling
    |   +-- master_scheduler.py    #   ECS Fargate + APScheduler
    +--
    +-- infra/                     # Infrastructure Adapters
    |   +-- db_adapter.py          #   PostgreSQL + Redis (JSON fallback)
    +--
    +-- config/                    # Configuration Constants
        +-- dshp_config.py         #   DSHP harvest thresholds
        +-- position_dependency_map.py # CDM entity dependency graph
        +-- scan_universe.py       #   Systematic scan ticker universe
```

## Orchestration Flow (main.py)

```
Phase 0:  Initialization + Overnight Gap Check
Phase 1:  Multi-Feed Data Ingestion (FRED, Crypto, PMI, SEC, RSS)
Phase 1.5: Live Portfolio Ingestion (IBKR positions + NAV)
Phase 2:  Macro Regime (ARAS, RPE, RSS, PDS, Correlation, PCR, Shutdown)
Phase 2.5: Anticipatory Intelligence (ELVT, JPVI, PFVT, SCCR)
Phase 3:  Portfolio Maintenance (SSL, DSHP, CDF)
Phase 4:  Hedge Management (FEM, CAM, CDM, PTRH)
Phase 5:  Thesis Integrity (CDM, TDC, TRP, PERM)
Phase 6:  Master Engine Rebalance (MICS, Gate3, PAIE, LAEP execution)
Phase 6.5: Growth & Re-Entry (ARES, AUP, SLOF)
Phase 7:  Consolidation & Reporting (Daily Monitor, EOD Snapshot)
```
