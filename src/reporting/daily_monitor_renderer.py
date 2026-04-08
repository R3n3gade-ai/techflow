from reporting.daily_monitor_view import DailyMonitorReportView

def render_html_report(view: DailyMonitorReportView) -> str:
    """
    Renders the DailyMonitorReportView into an institutional-grade HTML document.
    Designed for print-to-PDF or web viewing.
    """
    
    equity_rows = ""
    for row in view.equity_book:
        equity_rows += f"<tr><td><strong>{row.ticker}</strong></td><td>{row.name}</td><td>{row.weight}</td><td>{row.session}</td><td><span class='status {row.status.lower().replace(' ', '-').replace('/', '-')}'>{row.status}</span></td><td>{row.flag}</td></tr>"

    queue_rows = ""
    if not view.deployment_queue:
        queue_rows = "<tr><td colspan='5' style='text-align: center; font-style: italic;'>Queue Empty</td></tr>"
    else:
        for q in view.deployment_queue:
            queue_rows += f"<tr><td>{q.id_num}</td><td><strong>{q.ticker}</strong></td><td>{q.target}</td><td>{q.execution_instruction}</td><td>{q.trigger}</td></tr>"

    module_cards = ""
    for m in view.modules:
        module_cards += f"""
        <div class='card module-card'>
            <h4>{m.name}</h4>
            <div class='state-label'>{m.state_label}</div>
            <div class='sub-label'>{m.sub_label}</div>
            <p>{m.description}</p>
        </div>"""

    alerts_html = ""
    if not view.alerts:
        alerts_html = "<p><em>No active alerts.</em></p>"
    for a in view.alerts:
        alerts_html += f"<div class='alert-item'><strong>{a.title}</strong> — {a.body}</div>"

    decisions_html = ""
    for d in view.decisions:
        decisions_html += f"<div class='decision-item'><strong>{d.id_num}. {d.title}</strong><br><em>{d.body}</em></div>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap');
    
    :root {{
        --navy: #0A192F;
        --gold: #D4AF37;
        --cream: #FAF9F6;
        --dark-gray: #333333;
        --light-gray: #E8E8E8;
        --alert-red: #8B0000;
        --watch-orange: #CC5500;
        --ok-green: #006400;
    }}
    
    body {{
        font-family: 'Open Sans', sans-serif;
        background-color: #ffffff;
        color: var(--dark-gray);
        margin: 0;
        padding: 20px;
        font-size: 11px;
        line-height: 1.4;
    }}
    
    .container {{
        max-width: 900px;
        margin: 0 auto;
        background-color: var(--cream);
        border: 1px solid var(--gold);
        padding: 40px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    /* Masthead */
    .masthead {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 3px solid var(--navy);
        padding-bottom: 15px;
        margin-bottom: 20px;
    }}
    .masthead-left h1 {{
        font-family: 'Merriweather', serif;
        font-size: 24px;
        color: var(--navy);
        margin: 0 0 5px 0;
        text-transform: uppercase;
    }}
    .masthead-left p {{
        margin: 0;
        font-weight: 600;
        color: var(--dark-gray);
    }}
    .masthead-right {{
        background-color: var(--navy);
        color: white;
        padding: 15px 25px;
        text-align: center;
        border-left: 4px solid var(--gold);
    }}
    .masthead-right .regime-title {{
        font-size: 10px;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--gold);
    }}
    .masthead-right .regime-value {{
        font-family: 'Merriweather', serif;
        font-size: 20px;
        font-weight: 900;
        margin: 5px 0;
    }}
    .masthead-right .regime-score {{
        font-size: 12px;
        font-style: italic;
    }}
    
    /* Session Headline */
    .session-headline {{
        background-color: var(--navy);
        color: white;
        padding: 15px;
        border-left: 4px solid var(--gold);
        margin-bottom: 30px;
        font-family: 'Merriweather', serif;
        font-size: 12px;
        line-height: 1.6;
    }}
    .session-headline strong {{
        color: var(--gold);
        text-transform: uppercase;
    }}
    
    /* Section Headers */
    h2 {{
        font-family: 'Merriweather', serif;
        font-size: 14px;
        color: var(--navy);
        text-transform: uppercase;
        border-bottom: 1px solid var(--gold);
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 15px;
    }}
    
    /* Tables */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: white;
    }}
    th, td {{
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid var(--light-gray);
    }}
    th {{
        background-color: var(--navy);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 10px;
    }}
    
    /* Status Badges */
    .status {{
        font-weight: bold;
        text-transform: uppercase;
        font-size: 10px;
    }}
    .status.alert {{ color: var(--alert-red); }}
    .status.watch {{ color: var(--watch-orange); }}
    .status.ok {{ color: var(--ok-green); }}
    .status.intact {{ color: var(--ok-green); }}
    .status.impaired {{ color: var(--watch-orange); }}
    .status.broken {{ color: var(--alert-red); }}
    
    /* Macro Grid */
    .macro-grid {{
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 20px;
    }}
    .macro-card {{
        flex: 1;
        background-color: white;
        border: 1px solid var(--light-gray);
        border-top: 3px solid var(--gold);
        padding: 10px;
        text-align: center;
    }}
    .macro-card .title {{ font-size: 10px; text-transform: uppercase; color: var(--navy); font-weight: bold; }}
    .macro-card .value {{ font-size: 16px; font-weight: bold; margin: 5px 0; font-family: 'Merriweather', serif; }}
    
    /* Module Grid */
    .module-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }}
    .module-card {{
        background-color: white;
        border: 1px solid var(--light-gray);
        padding: 12px;
        border-top: 3px solid var(--navy);
    }}
    .module-card h4 {{ margin: 0 0 5px 0; color: var(--navy); font-size: 12px; }}
    .module-card .state-label {{ font-weight: bold; color: var(--navy); margin-bottom: 2px; }}
    .module-card .sub-label {{ font-family: 'Merriweather', serif; font-weight: bold; font-size: 14px; margin-bottom: 8px; }}
    .module-card p {{ margin: 0; font-size: 10px; color: #555; }}
    
    /* Lists */
    .alert-item, .decision-item {{
        margin-bottom: 10px;
        padding-left: 10px;
        border-left: 3px solid var(--gold);
    }}
    
    .footer {{
        margin-top: 40px;
        padding-top: 15px;
        border-top: 1px solid var(--gold);
        font-size: 9px;
        color: #777;
        text-align: center;
        font-style: italic;
    }}
</style>
</head>
<body>

<div class="container">

    <div class="masthead">
        <div class="masthead-left">
            <h1>ACHELION ARMS — Daily Monitor</h1>
            <p>{view.report_date} &middot; {view.quarter_day} &middot; {view.architecture_version} &middot; {view.operator_context}</p>
            <p style="color: var(--gold); margin-top: 5px;"><strong>{view.headline_event}</strong></p>
        </div>
        <div class="masthead-right">
            <div class="regime-title">REGIME</div>
            <div class="regime-value">{view.regime_transition}</div>
            <div class="regime-score">Score est. {view.regime_score_str}</div>
            <div class="regime-title" style="margin-top: 5px; color: white;">{view.regime_sub_status}</div>
        </div>
    </div>

    <div class="session-headline">
        <strong>SESSION HEADLINE — </strong> {view.session_headline}
    </div>

    <h2>1 &middot; MACRO COMPASS — REGIME SCORING</h2>
    <table>
        <tr><th>Current Score</th><th>Prior Score</th><th>Equity Ceiling</th><th>Queue Trigger</th><th>ARES Status</th></tr>
        <tr><td><strong>{view.current_score}</strong></td><td>{view.prior_score}</td><td>{view.equity_ceiling}</td><td>{view.queue_trigger}</td><td>{view.ares_status}</td></tr>
    </table>
    <p style="font-style: italic; font-size: 10px;">Score drivers: {view.score_drivers}</p>

    <h2>2 &middot; MACRO INPUTS</h2>
    <div class="macro-grid">
        <div class="macro-card"><div class="title">S&P 500 Futures</div><div class="value">{view.sp500_futures}</div></div>
        <div class="macro-card"><div class="title">Nasdaq Futures</div><div class="value">{view.nasdaq_futures}</div></div>
        <div class="macro-card"><div class="title">Brent Crude</div><div class="value">{view.brent_crude}</div></div>
        <div class="macro-card"><div class="title">VIX</div><div class="value">{view.vix}</div></div>
        <div class="macro-card"><div class="title">10Y Treasury</div><div class="value">{view.treasury_10y}</div></div>
    </div>

    <h2>3 &middot; EQUITY BOOK — CEILING {view.equity_ceiling}</h2>
    <table>
        <tr><th>Ticker</th><th>Name</th><th>Wt.</th><th>Action</th><th>Status</th><th>Flag</th></tr>
        {equity_rows}
    </table>

    <h2>4 &middot; DEPLOYMENT QUEUE — TRIGGER {view.queue_trigger}</h2>
    <table>
        <tr><th>#</th><th>Ticker</th><th>Target</th><th>Execution Instruction</th><th>Trigger</th></tr>
        {queue_rows}
    </table>

    <h2>5 &middot; DEFENSIVE SLEEVE + PTRH + CASH</h2>
    <div class="macro-grid" style="text-align: left;">
        <div style="flex: 1; padding: 10px;">
            <strong>SGOV:</strong> {view.sgov_weight} (T-bill ETF)<br>
            <strong>SGOL:</strong> {view.sgol_weight} (Gold)<br>
            <strong>DBMF:</strong> {view.dbmf_weight} (Managed futures)<br>
            <strong>STRC:</strong> {view.strc_weight}
        </div>
        <div style="flex: 1; padding: 10px; border-left: 1px solid var(--gold);">
            <strong>PTRH — QQQ Puts</strong><br>
            <span style="font-size: 14px; font-family: 'Merriweather', serif; color: var(--navy); font-weight: bold;">{view.ptrh_status_str}</span><br>
            <span style="font-size: 10px;">Autonomously scaled via CAM protocol</span>
        </div>
        <div style="flex: 1; padding: 10px; border-left: 1px solid var(--gold);">
            <strong>Cash — {view.cash_weight}</strong><br>
            <span style="font-size: 10px;">{view.cash_context}</span>
        </div>
    </div>

    <h2>6 &middot; MODULE STATUS</h2>
    <div class="module-grid">
        {module_cards}
    </div>

    <h2>7 &middot; ALERTS</h2>
    {alerts_html}

    <h2>8 &middot; PM DECISION QUEUE</h2>
    {decisions_html}

    <div class="footer">
        Data sourced from public markets &middot; {view.report_date} &middot; Regime: {view.regime_transition} &middot; Score {view.regime_score_str} &middot; {view.architecture_version} &middot; Achelion Capital Management, LLC &middot; CONFIDENTIAL — For GP and Development Use Only
    </div>

</div>
</body>
</html>
"""
    return html
