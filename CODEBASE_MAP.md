### Achelion ARMS: Codebase Map & Architecture (Updated April 8, 2026)

```
achelion_arms/
│
├── 📄 CODEBASE_MAP.md              # This file: A visual map of the entire project.
├── 📄 MASTER_IMPLEMENTATION_PLAN.md # The live tracker of what has been implemented.
│
├── 📁 docs/                         # Contains all the detailed specification and strategy documents.
│   ├── 📄 ARMS_COMPLETE_SYSTEM_ARCHITECTURE.mermaid # The canonical 7-layer architecture diagram (April 8).
│   ├── 📄 ARMS_COMPREHENSIVE_CHECKPOINT_AUDIT_2026-04-08.md # The exhaustive audit confirming all modules.
│   ├── 📄 understanding_arms_gp_briefing_updated.md # The plain-language GP briefing document.
│   ├── 📄 ARMS_FSD_Master_Build_Document_v1.1.md
│   └── 📄 ... (All Addenda 1-6 and historical audits)
│
├── 📁 data/                        # Contains the JSON state overlays and config maps
│   ├── 📄 mj_portfolio_snapshot.json # The live portfolio state override for matching MJ's report.
│   ├── 📄 mj_pm_notes.json         # The editorial bridge file for PM narrative insertion.
│   └── 📄 mj_strategic_queue.json  # The staged proactive deployment queue items.
│
├── 📁 SAMPLES/                     # Sample outputs
│   └── 📄 daily_monitor_mj_exact.html # The rendered institutional PDF-style report.
│
└── 📁 src/                         # The main folder for all of our working Python code.
    │
    ├── 🐍 main.py                  # The Orchestrator: Wires all 7 layers together.
    │
    ├── 📁 data_feeds/              # 🧠 L1: THE SENSES
    │   ├── 🐍 pipeline.py          # Aggregates feeds into a single data stream.
    │   ├── 🐍 fred_plugin.py       # Live macro data from the Federal Reserve API.
    │   ├── 🐍 sec_edgar_feed.py    # Form 4 Insider Trades.
    │   └── 🐍 news_rss_feed.py     # Live event bridges (geopolitics, earnings).
    │
    ├── 📁 engine/                  # 🧠 L2 & L3: THE NAVIGATOR & THE PILLARS
    │   ├── 🐍 macro_compass.py     # L2: Regime Scoring Engine (0.0 to 1.0).
    │   ├── 🐍 aras.py              # L2: Converts score to Regime & Equity Ceiling.
    │   ├── 🐍 drawdown_sentinel.py # L3 (PDS): Hard NAV drawdown stop (-12% / -18%).
    │   ├── 🐍 kevlar.py            # L3: 22% single-name concentration limit.
    │   ├── 🐍 tail_hedge.py        # L3 (PTRH): Delta-primary (-0.35) options scanner.
    │   ├── 🐍 cam.py               # L3: Autonomous tail hedge sizing multiplier.
    │   ├── 🐍 dshp.py              # L3: Defensive sleeve gain harvester.
    │   ├── 🐍 cdm.py               # L3: Customer Dependency Map (signal propagation).
    │   ├── 🐍 tdc.py               # L3: Thesis Dependency Checker (thesis integrity).
    │   ├── 🐍 ares.py              # L3: Re-Entry System (3-gate clearance).
    │   ├── 🐍 cdf.py               # L3: Conviction Decay Function (10pp underperformance logic).
    │   ├── 🐍 perm.py              # L3: Covered Call yield harvester.
    │   ├── 🐍 slof.py              # L3: Synthetic Leverage Overlay (1.25x).
    │   ├── 🐍 mics.py              # L3: Model-Implied Conviction Score logic.
    │   └── 🐍 master_engine.py     # L4: Portfolio Builder (calculates ideal weights).
    │
    ├── 📁 intelligence/            # 🧠 L3: THE ANALYST
    │   └── 🐍 llm_wrapper.py       # Universal LLM Bridge (Anthropic, OpenAI, Google) for TDC/SENTINEL.
    │
    ├── 📁 execution/               # 🧠 L5 & L6: THE NERVES & MUSCLES
    │   ├── 🐍 order_book.py        # L5: LAEP (Liquidity-Adjusted Execution Protocol).
    │   ├── 🐍 strategic_queue.py   # L5: Proactive regime-triggered deployment queue.
    │   ├── 🐍 circuit_breaker.py   # L5: Hard intraday stops (SPX -5% / VIX >30).
    │   ├── 🐍 broker_api.py        # L6: The IBKR adapter for placing live paper trades.
    │   └── 🐍 confirmation_queue.py# L5: The secure inbox for PM Tier 1 actions.
    │
    └── 📁 reporting/               # 🧠 L7: THE MEMORY & VOICE
        ├── 🐍 audit_log.py         # Immutable JSON log of every system decision.
        ├── 🐍 daily_monitor.py     # Aggregates L1-L6 data into the daily payload.
        ├── 🐍 daily_monitor_view.py# Formats payload matching MJ's specs.
        └── 🐍 daily_monitor_renderer.py # Renders the HTML document.
```
