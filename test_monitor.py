import json
from src.reporting.daily_monitor import run_daily_monitor

market_context = """
The ceasefire between Iran and Israel is fracturing on day one. Iran's IRGC suspended the shipping coordination protocol (the core ceasefire deliverable) after Israel continued strikes on Lebanon near Tyre and Sidon. Iran's parliament speaker Ghalibaf claims three provisions are violated (primarily Lebanon). Hormuz remains effectively closed, with MarineTraffic showing only a handful of vessels and a 1,000-ship backlog not clearing. Oil has reversed: WTI +3% to ~$97, Brent ~$98. Equity futures are down -0.4%. Vance, Witkoff, and Kushner are heading to Islamabad Saturday for the first direct US-Iran talks in the modern era. Vance says Ghalibaf's complaints show 'there's a lot of agreement'. Iran prefers Vance over the others. Pakistan is in diplomatic lockdown for the talks. PCE inflation data is due today (Fed's Jefferson notes oil complicates the outlook). Lebanon is the structural fault line.
"""

raw_inputs = {
    "date": "April 9, 2026",
    "regime": "DEFENSIVE",
    "score": 0.74,
    "score_direction": "↑",
    "queue_status": "LOCKED",
    "macro_compass_score_yesterday": 0.72,
    "macro_compass_trigger": 0.65,
    "macro_compass_next_catalyst": "Islamabad · Sat (Vance leads US delegation)",
    "macro_compass_drivers_up": "Hormuz effectively still closed · IRGC suspended tanker coordination after Lebanon strikes · Iran parliament speaker claims 3 ceasefire violations · Israel continuing Lebanon operations · Oil +3% reversal to ~$97–98 Brent · Equity futures –0.4% · Lebanon dispute creates structural ceasefire ambiguity.",
    "macro_compass_drivers_down": "Two-week ceasefire framework intact · Islamabad Saturday with senior US delegation · VIX lower than pre-ceasefire · Goldman Sachs trimmed Q2 oil forecasts to $90/$87 · Vance noted signs Hormuz may begin reopening · Iran prefers Vance at the table.",
    "macro_inputs": {
        "S&P 500 futures": {"value": "-0.4%", "context": "Ceasefire skepticism. Yesterday's +2.51% close giving back. Reality setting in."},
        "Brent crude": {"value": "~$98", "context": "REVERSAL: +3% from yesterday's $94 low. Hormuz still closed. Oil signal re-escalating."},
        "WTI crude": {"value": "~$97", "context": "+3% reversal. Goldman Q2 forecast $87. Spot recovering as Hormuz violation confirmed."},
        "VIX": {"value": "~22–24", "context": "At NORMAL/ELEVATED boundary (threshold: 25). Watch for VIX break above 25."},
        "Hormuz status": {"value": "CLOSED", "context": "IRGC suspended coordination after Lebanon strikes. ~1,000 ships backlogged. Key ceasefire condition unmet."},
        "Islamabad talks": {"value": "Saturday", "context": "Vance + Witkoff + Kushner. Iran prefers Vance. Pakistan in full diplomatic lockdown. Red Zone sealed."},
        "PCE Inflation": {"value": "Today", "context": "Fed’s preferred inflation gauge due Thursday. Jefferson: oil complicates inflation outlook."},
        "Lebanon dispute": {"value": "CRITICAL", "context": "Iran: Lebanon in ceasefire. US/Israel: Lebanon excluded. Iran FM: 'US must choose.' Structural fault line."}
    },
    "equity_book": [
        {"ticker": "TSLA", "name": "Tesla", "weight": 8.8, "session_perf": -0.8, "status": "OK", "rationale": "Giving back part of yesterday’s +3.5%. No thesis change. IRGC threat partially reinstated with Lebanon strikes."},
        {"ticker": "NVDA", "name": "Nvidia", "weight": 7.8, "session_perf": -0.6, "status": "OK", "rationale": "AI capex thesis intact. Ceasefire skepticism weighing on broad tech. No position-specific flag."},
        {"ticker": "AMD", "name": "Adv. Micro Devices", "weight": 7.2, "session_perf": -0.7, "status": "OK", "rationale": "Thesis intact. Broad tech weakness."},
        {"ticker": "PLTR", "name": "Palantir", "weight": 5.7, "session_perf": 0.3, "status": "OK", "rationale": "Outperforming today. Lebanon re-escalation and continued conflict incrementally positive for DOD AI spend thesis."},
        {"ticker": "ALAB", "name": "Astera Labs", "weight": 3.42, "session_perf": -0.5, "status": "TRIMMED", "rationale": "Trimmed correctly. SENTINEL re-check required before any re-add. No new action."},
        {"ticker": "MU", "name": "Micron", "weight": 4.5, "session_perf": -0.9, "status": "OK", "rationale": "TDC closed · TIS INTACT (8.2). Memory demand thesis unaffected by ceasefire dynamics."},
        {"ticker": "ANET", "name": "Arista Networks", "weight": 4.3, "session_perf": -0.4, "status": "OK", "rationale": "Thesis intact. Hyperscaler capex unaffected."},
        {"ticker": "AVGO", "name": "Broadcom", "weight": 3.7, "session_perf": -0.3, "status": "THESIS+", "rationale": "Google + Anthropic deals intact. THESIS+ maintained from yesterday."},
        {"ticker": "MRVL", "name": "Marvell Tech", "weight": 3.5, "session_perf": -0.5, "status": "THESIS+", "rationale": "NVDA $2B + AVGO validation intact. TIS INTACT. THESIS+ maintained."},
        {"ticker": "ARM", "name": "Arm Holdings", "weight": 2.5, "session_perf": -0.6, "status": "OK", "rationale": "Thesis intact."},
        {"ticker": "ETN", "name": "Eaton Corp", "weight": 2.0, "session_perf": 0.2, "status": "OK", "rationale": "Power infrastructure thesis long-cycle. Slight outperformance. Conflict duration extends electrification thesis."},
        {"ticker": "VRT", "name": "Vertiv", "weight": 2.3, "session_perf": -0.3, "status": "QUEUED", "rationale": "$15B backlog intact. Queue size-up to 3.0% locked pending NEUTRAL trigger."}
    ],
    "deployment_queue": [
        {"ticker": "GOOGL", "target": "4.5–5.0%", "execution_instruction": "3.5% at NEUTRAL trigger via VWAP · Leg 2: +1.5% on positive April 28 earnings · EVENT-triggered", "status": "LOCKED · Score re-elevating"},
        {"ticker": "GEV", "target": "2.5–3.0%", "execution_instruction": "60% at trigger VWAP · Leg 2: 40% on flush to $820–840 · PRICE-triggered", "status": "LOCKED"},
        {"ticker": "CEG", "target": "2.0–2.5%", "execution_instruction": "Full size at trigger · VWAP · Single-leg", "status": "LOCKED"},
        {"ticker": "VST", "target": "1.5–2.0%", "execution_instruction": "Full size at trigger · VWAP · Single-leg", "status": "LOCKED"},
        {"ticker": "VRT (+add)", "target": "2.3%→3.0%", "execution_instruction": "Size-up existing position · Limit add", "status": "LOCKED"}
    ],
    "defensive_sleeve": [
        {"ticker": "SGOV", "weight": 3.0, "rationale": "Stable. Earns yield. No action required."},
        {"ticker": "SGOL", "weight": 2.0, "rationale": "Gold holding ceasefire gains. Dollar still relatively weak. Safe haven demand persists."},
        {"ticker": "DBMF", "weight": 5.0, "rationale": "Oil +3% today POSITIVE for long oil trend. Yesterday’s reversal risk has cleared. Monitor oil direction."},
        {"ticker": "STRC", "weight": 4.0, "rationale": "11.5% yield · Regime reserve intact · Unlocks at NEUTRAL — not today."},
        {"ticker": "PTRH", "weight": 1.5, "rationale": "DEFENSIVE confirmed. Ceasefire fracture means tail hedge still earning its cost. Do not reduce. 5–8% OTM · DTE 60–90 · Roll at 30 DTE. Confirm all contracts ≥30 DTE."},
        {"ticker": "Cash", "weight": 8.0, "rationale": "Fully intact. Queue locked. No deployment today. STRC reserve earning yield while we wait. Patient capital earns the entry price."}
    ],
    "module_status": {
        "ARAS": {"status": "Re-elevating DEFENSIVE ~0.74↑", "detail": "Score moved from ~0.85 to ~0.72 yesterday, now re-elevating to ~0.74 as Hormuz closure confirmed and oil reverses +3%. ARES running 5-min cycles. Queue trigger moving further away, not closer."},
        "ARES": {"status": "Queue LOCKED", "detail": "Score re-elevating. Requires 3 consecutive cycles ≤0.65. Currently ~9 points away. Saturday Islamabad is next potential catalyst for score decline."},
        "DBMF": {"status": "Oil +3% CLEARED", "detail": "Yesterday’s oil reversal risk has resolved. Oil +3% today is favorable for DBMF’s long oil trend position. DSHP harvest alert cleared. Continue monitoring oil direction."},
        "CAM": {"status": "PTRH 1.5× CONFIRMED", "detail": "DEFENSIVE regime confirmed. PTRH at 1.5×. CAM recalculating with Brent $98 and re-elevating macro stress. Asymmetric 15% tolerance prevents premature reduction."},
        "LAEP": {"status": "Mode NORMAL/ELEVATED", "detail": "VIX ~22–24 at boundary (threshold: 25). If ceasefire fractures further and VIX breaks above 25, LAEP returns to ELEVATED: 60-min VWAP windows, 20bps slippage."},
        "FEM": {"status": "Status NO FLAGS", "detail": "All 12 positions within concentration parameters. No new FEM alert. Queue preflight runs automatically when ARES confirms trigger — not today."}
    }
}

print("Running rendering test...")
markdown_output = run_daily_monitor(raw_inputs, market_context)

with open("/data/.openclaw/workspace/achelion_arms/SAMPLES/daily_monitor_20260409.md", "w") as f:
    f.write(markdown_output)

print("Saved to SAMPLES/daily_monitor_20260409.md")
