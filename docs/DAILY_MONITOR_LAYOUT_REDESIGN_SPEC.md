# Achelion ARMS Daily Monitor Layout Redesign Spec

## Goal
Design the ARMS Daily Monitor to match the externally supplied sample layout as closely as practical while preserving ARMS data-model integrity.

Reference sample:
- `docs/daily_report_sample_layout_2026-04-01.md`
- user also supplied an image showing the visual layout

## Product Direction
The Daily Monitor should feel like:
- an institutional pre-market PDF briefing
- a printable partner-facing operating document
- a structured morning instrument, not a generic dashboard

It should NOT feel like:
- a consumer web dashboard
- a loose collection of widgets
- a developer-only JSON dump

## Canonical Section Order for New Daily Monitor
1. Header / masthead
2. Session headline
3. Macro Compass — Regime Scoring
4. Macro Inputs
5. Equity Book
6. Deployment Queue
7. Defensive Sleeve + PTRH + Cash
8. Module Status
9. Alerts
10. PM Decision Queue
11. Footer / confidentiality line

## Visual System
### Core palette
- **Navy / near-black header background** for title block
- **Warm cream / parchment panels** for content cards
- **Gold / amber accents** for borders, section dividers, and emphasis text
- **Red/orange** for high-risk / crash / alert states
- **Green** for positive / intact / improving states
- **Muted gray-blue** for secondary metadata and table labels

### Typography
- Strong uppercase section labels
- Bold display treatment for regime, score, and title
- Dense but readable report typography
- Narrow vertical rhythm, optimized for printable PDF pages

### Layout style
- Page-oriented layout with repeatable page header/footer
- Wide content sections broken by strong rules/dividers
- Summary boxes at top of major sections
- Tables for book, queue, and status-heavy content
- Cards for module status and macro inputs

## Mapping Existing ARMS Data Model to New Layout
Current `DailyMonitor` payload fields from `src/reporting/daily_monitor.py`:
- `timestamp`
- `regime`
- `regime_score`
- `rpe`
- `ptrh`
- `dshp_alerts`
- `cdm_alerts`
- `tdc_reviews`
- `mics_summary`
- `ares_status`
- `cdf_summary`
- `retail_sentiment`
- `safety_status`
- `decision_queue`
- `portfolio_summary`

These are enough to seed a redesign, but not enough on their own to perfectly render the sample. We need a richer view-model.

## Proposed Presentation View-Model
Create a report-specific view-model layer that sits between raw engine outputs and the final renderer.

Suggested structure:

```python
@dataclass
class DailyMonitorReportView:
    header: HeaderView
    headline: HeadlineView
    macro_compass: MacroCompassView
    macro_inputs: list[MacroInputCard]
    equity_book: list[EquityRowView]
    deployment_queue: list[QueueRowView]
    defensive_sleeve: DefensiveSleeveView
    module_status: list[ModuleStatusCard]
    alerts: list[AlertView]
    pm_decision_queue: list[DecisionItemView]
    footer: FooterView
```

## Section-by-Section Design

### 1. Header / Masthead
**Visual target:** same split masthead as sample.

Left block:
- main title: `ACHELION ARMS — Daily Monitor`
- formatted date
- quarter/day label
- architecture version
- operator/developer context if desired
- one line for the highest-priority event of the day

Right block:
- regime state shown large
- transition if applicable (e.g. `CRASH → DEFENSIVE`)
- score estimate / precise score
- one short sub-status line (e.g. `Boundary crossed · ARES confirming`)

Data sources:
- `regime`, `regime_score`, `ares_status`, plus calendar/date formatting

### 2. Session Headline
Narrative paragraph summarizing the morning state.

Should include:
- what happened overnight / prior session
- major market moves
- most important catalyst
- what the score implies operationally

Source:
- likely generated summary function or AI narrative pass using macro data + regime + alerts

### 3. Macro Compass — Regime Scoring
Top summary strip with five compact boxes, matching the sample.

Suggested fields:
- Current Score
- Prior Score
- Equity Ceiling
- Queue Trigger
- ARES Status

Supporting text below:
- score drivers
- partial offsets
- regime key thresholds

Source mapping:
- `regime`, `regime_score`, `rpe`, `ares_status`
- additional prior-score and equity ceiling data may need to be added upstream

### 4. Macro Inputs
Grid of compact cards.

Likely fields:
- S&P 500 futures
- Nasdaq futures
- VIX
- Brent crude
- 10Y Treasury
- major event clock / speech / earnings
- employment / macro print
- geopolitical threat state

Current code gap:
- existing `DailyMonitor` payload does not explicitly carry this presentation-ready macro bundle
- add a dedicated `macro_inputs` structure sourced from data pipeline and contextual news layer

### 5. Equity Book
A structured table matching the sample’s feel.

Columns:
- Ticker
- Name
- Weight
- Session
- Status
- Flag

Potential additional internal fields:
- thesis status
- TIS
- target weight
- review due date
- CDM/TDC notes

Source gap:
- current `portfolio_summary` is too coarse; needs per-position view data from master engine / portfolio snapshot

### 6. Deployment Queue
Table of queued deployment candidates and trigger conditions.

Columns:
- #
- Ticker
- Target
- Execution Instruction
- Trigger

Source gap:
- current generic `decision_queue` is insufficient for a rich deployment table
- likely needs separate queue data for ARES / regime-triggered deployment plans vs immediate PM review items

### 7. Defensive Sleeve + PTRH + Cash
Dedicated section summarizing safe assets, hedge posture, and cash structure.

Blocks:
- defensive sleeve components and weights
- PTRH posture / target multiple / CAM status
- cash buckets and commentary

Source mapping:
- `ptrh`
- `portfolio_summary`
- DSHP-related data
- likely additional sleeve allocation detail from portfolio engine

### 8. Module Status
Card grid for module-level operational state.

Candidate modules:
- ARAS
- ARES
- TDC
- CAM / PTRH
- LAEP
- FEM
- CDF
- Safety / incapacitation

Each card should contain:
- module name
- state label
- one-line interpretation
- one short operational implication

Source mapping:
- `ares_status`, `tdc_reviews`, `cdf_summary`, `safety_status`, `ptrh`, `cdm_alerts`, etc.

### 9. Alerts
Long-form narrative alerts, each with a strong title and paragraph body.

Alert priority examples:
- geopolitical catalyst
- regime transition significance
- CDM high-severity event
- overdue thesis review

Source mapping:
- `cdm_alerts`, `tdc_reviews`, regime transitions, safety states
- likely generated narrative layer needed to produce polished institutional prose

### 10. PM Decision Queue
Human-readable action list.

Format should match sample:
- numbered items
- one-line action title
- short follow-on explanation
- explicit whether action is required or no action required

Source mapping:
- `decision_queue`
- plus synthesized recommendations from TDC/CDF/ARES/regime state

## Engineering Recommendation
Do not cram this directly into the current `DailyMonitor` dataclass.

Instead:
1. keep `DailyMonitor` as the raw aggregation payload
2. add a new transformation layer, e.g. `src/reporting/daily_monitor_view.py`
3. create a renderer, e.g. `src/reporting/daily_monitor_template.html` or markdown/PDF template
4. support both:
   - web-rendered dashboard view
   - PDF export preserving page style

## Proposed New Files
- `src/reporting/daily_monitor_view.py`
  - converts raw monitor payload into report-ready view model
- `src/reporting/daily_monitor_renderer.py`
  - renders HTML/markdown/PDF payload
- `src/reporting/templates/daily_monitor.html`
  - print-first HTML template matching sample
- `src/reporting/styles/daily_monitor.css`
  - gold/navy/cream design system
- optionally `src/reporting/sample_data/` for fixture payloads

## Immediate Build Plan
### Phase A — Save and lock reference
- [x] Save supplied sample text to repo
- [ ] Save/attach visual screenshot reference into repo if available as a file

### Phase B — View-model expansion
- [ ] Define richer `DailyMonitorReportView` dataclasses
- [ ] Add macro input section model
- [ ] Add per-position equity book model
- [ ] Add deployment queue model
- [ ] Add module status card model
- [ ] Add alert narrative model

### Phase C — Rendering layer
- [ ] Build print-first HTML template matching sample layout
- [ ] Implement CSS tokens and page styling
- [ ] Support page header/footer repetition for PDF export
- [ ] Add section numbering and table styles

### Phase D — Data plumbing
- [ ] Add upstream data required for macro input cards
- [ ] Add portfolio snapshot detail for equity book
- [ ] Add target/trigger metadata for deployment queue
- [ ] Add prior-score and boundary metadata for macro compass
- [ ] Add narrative generation helpers for headline and alerts

### Phase E — Validation
- [ ] Create fixture from the supplied sample scenario
- [ ] Generate ARMS version using same layout
- [ ] Compare visually against sample image
- [ ] Tune spacing/typography/colors until the feel matches

## Important Constraint
The user explicitly wants ARMS daily reports to keep the same layout as the provided sample. Future design changes should preserve this layout unless the user says otherwise.
