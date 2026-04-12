> **? STALE DOCUMENT — NOT AUTHORITATIVE**
> This document predates significant code changes (April 2026 remediation cycle).
> For current system truth, see: ARMS_NEXT_WAVE_COLD_TRUTH_AUDIT_2026-04-10.md
> and ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md

# Achelion ARMS - Daily Monitor Redesign Implementation

## Objective
Convert the raw `DailyMonitor` dataclass payload from `src/reporting/daily_monitor.py` into a highly structured, institutional-grade markdown/HTML report view that exactly matches the provided visual layout reference from April 1, 2026.

## Requirements
- Parse `DailyMonitor` dataclass.
- Construct the `ReportView` layer.
- Render the split-header masthead (Title, Date, Version, Regime state, Score, Transition).
- Render the `Session Headline`.
- Render `Macro Compass` summary strip (Score drivers, boundaries).
- Render `Macro Inputs` cards (Futures, VIX, Crude, 10Y).
- Render `Equity Book` table (Ticker, Name, Weight, Session, Status, Flag).
- Render `Deployment Queue` table.
- Render `Defensive Sleeve + PTRH + Cash` summary.
- Render `Module Status` cards.
- Render `Alerts` narrative.
- Render `PM Decision Queue`.
- Output as a styled HTML document or clean Markdown matching the PDF-feel.

## Implementation Path
1. Create `src/reporting/daily_monitor_view.py` containing the `DailyMonitorReportView` models.
2. Create `src/reporting/daily_monitor_renderer.py` containing the logic to ingest the payload and format the string.
3. Update `main.py` to optionally print/save the rendered output instead of the raw dataclass.
