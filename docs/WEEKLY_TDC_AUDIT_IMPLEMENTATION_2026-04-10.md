# Weekly TDC Audit Implementation — 2026-04-10

## What changed
The weekly TDC audit path is no longer a stub.

`run_weekly_tdc_audit(all_positions)` now:
- builds a weekly audit alert for each equity ticker
- pulls recent SEC filing context via `sec_edgar_plugin.fetch_docs(...)`
- reuses the TDC review engine to produce a thesis-integrity judgment
- logs a `TDC_WEEKLY_AUDIT` event to the immutable session log
- writes durable TDC state via the same TDC persistence path

## Why this matters
Before:
- TDC was only reactive to propagated CDM alerts
- no scheduled broad thesis sweep existed

After:
- ARMS has a first durable proactive thesis-audit path
- weekly review can degrade names to monitor/remove even without a single acute CDM trigger

## Current limitation
This is a first implementation and still has constraints:
1. it uses SEC filing context as the main weekly audit evidence source, which is incomplete
2. it runs inline in the main cycle right now rather than on its own dedicated schedule
3. it should eventually include curated recent news + filings + thesis state together
4. `run_thesis_review()` still defaults some metadata for weekly alerts and should be refined further
