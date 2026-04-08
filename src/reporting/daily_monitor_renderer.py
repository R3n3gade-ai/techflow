from reporting.daily_monitor_view import DailyMonitorReportView

def render_html_report(view: DailyMonitorReportView) -> str:
    equity_rows = ""
    for row in view.equity_book:
        # Handling the multi-line ticker stuff (VRT +add / NVDA eval)
        ticker_html = row.ticker.replace("\n", "<br><span style='font-weight:normal; font-size:9px;'>")
        if "\n" in row.ticker: ticker_html += "</span>"
        
        equity_rows += f"<tr><td><strong>{ticker_html}</strong></td><td>{row.name}</td><td>{row.weight}</td><td style='color: var(--ok-green); font-weight:bold;'>{row.premkt}</td><td><span class='status {row.status.lower().replace('?', '').replace('+', '-plus')}'>{row.status}</span></td><td style='font-size:10px;'>{row.flag}</td></tr>"

    queue_rows = ""
    for q in view.deployment_queue:
        ticker_html = q.ticker.replace("\n", "<br><span style='font-weight:normal; font-size:9px;'>")
        if "\n" in q.ticker: ticker_html += "</span>"
        
        queue_rows += f"<tr><td>{q.id_num}</td><td><strong>{ticker_html}</strong></td><td>{q.target}</td><td style='font-size:10px;'>{q.execution_instruction}</td><td style='font-size:10px;'>{q.trigger.replace(' \u00b7 ', '<br>')}</td></tr>"

    module_cards = ""
    for m in view.modules:
        # Split title for styling
        parts = m.name.split(" \u00b7 ")
        title_main = parts[0]
        title_sub = parts[1] if len(parts) > 1 else ""
        
        module_cards += f"""
        <div class='card module-card'>
            <h4>{title_main} <span style='font-weight:normal; font-size:10px; color:#555;'>&middot; {title_sub}</span></h4>
            <div class='sub-label'>{m.state_label}</div>
            <p>{m.description}</p>
        </div>"""

    alerts_html = ""
    for a in view.alerts:
        alerts_html += f"<div class='alert-item'><strong>{a.title}</strong> &mdash; {a.body}</div>"

    decisions_html = ""
    for d in view.decisions:
        decisions_html += f"<div class='decision-item'><strong>{d.id_num}. {d.title}</strong><br><em>{d.body}</em></div>"

    # Macro Cards Grid
    mc = view.macro_cards
    macro_grid_html = f"""
    <div class="macro-grid-8">
        <div class="macro-card"><div class="title">S&P 500 Futures</div><div class="value positive">{mc.get('sp500',{}).get('value','')}</div><div class="sub">{mc.get('sp500',{}).get('sub','')}</div></div>
        <div class="macro-card"><div class="title">Brent Crude</div><div class="value negative">{mc.get('brent',{}).get('value','')}</div><div class="sub">{mc.get('brent',{}).get('sub','')}</div></div>
        <div class="macro-card"><div class="title">WTI Crude</div><div class="value negative">{mc.get('wti',{}).get('value','')}</div><div class="sub">{mc.get('wti',{}).get('sub','')}</div></div>
        <div class="macro-card"><div class="title">10Y Treasury</div><div class="value">{mc.get('treasury',{}).get('value','')}</div><div class="sub">{mc.get('treasury',{}).get('sub','')}</div></div>
        
        <div class="macro-card"><div class="title">Nasdaq Futures</div><div class="value positive">{mc.get('nasdaq',{}).get('value','')}</div><div class="sub">{mc.get('nasdaq',{}).get('sub','')}</div></div>
        <div class="macro-card"><div class="title">VIX</div><div class="value">{mc.get('vix',{}).get('value','')}</div><div class="sub">{mc.get('vix',{}).get('sub','')}</div></div>
        <div class="macro-card"><div class="title">Islamabad Talks</div><div class="value">{mc.get('talks',{}).get('value','')}</div><div class="sub">{mc.get('talks',{}).get('sub','')}</div></div>
        <div class="macro-card"><div class="title">Hormuz Status</div><div class="value">{mc.get('hormuz',{}).get('value','')}</div><div class="sub">{mc.get('hormuz',{}).get('sub','')}</div></div>
    </div>
    """

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
        --light-blue: #E6F0FA;
    }}
    
    body {{
        font-family: 'Open Sans', sans-serif;
        background-color: #ffffff;
        color: var(--dark-gray);
        margin: 0;
        padding: 20px;
        font-size: 11px;
        line-height: 1.5;
    }}
    
    .container {{
        max-width: 900px;
        margin: 0 auto;
        background-color: var(--cream);
        border: 1px solid var(--gold);
        padding: 40px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .masthead-top {{
        font-size: 9px;
        text-transform: uppercase;
        color: var(--navy);
        border-bottom: 1px solid var(--navy);
        padding-bottom: 5px;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
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
        font-size: 26px;
        color: var(--navy);
        margin: 0 0 5px 0;
        text-transform: uppercase;
        letter-spacing: -0.5px;
    }}
    .masthead-left p {{
        margin: 0;
        font-weight: 600;
        color: var(--dark-gray);
        font-size: 12px;
    }}
    .masthead-right {{
        background-color: var(--navy);
        color: white;
        padding: 15px 25px;
        text-align: center;
        border-left: 4px solid var(--gold);
        min-width: 150px;
    }}
    .masthead-right .regime-title {{
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--gold);
    }}
    .masthead-right .regime-value {{
        font-family: 'Merriweather', serif;
        font-size: 18px;
        font-weight: 900;
        margin: 5px 0;
    }}
    .masthead-right .regime-score {{
        font-size: 11px;
    }}
    
    /* Session Headline */
    .session-headline {{
        background-color: var(--light-blue);
        color: var(--navy);
        padding: 15px;
        border-left: 4px solid var(--navy);
        margin-bottom: 30px;
        font-size: 11px;
    }}
    .session-headline strong {{
        font-family: 'Merriweather', serif;
        text-transform: uppercase;
    }}
    
    /* Section Headers */
    h2 {{
        font-family: 'Merriweather', serif;
        font-size: 13px;
        color: var(--navy);
        text-transform: uppercase;
        border-bottom: 1px solid var(--gold);
        padding-bottom: 5px;
        margin-top: 35px;
        margin-bottom: 15px;
        letter-spacing: 1px;
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
        vertical-align: top;
    }}
    th {{
        background-color: var(--light-blue);
        color: var(--navy);
        font-weight: 700;
        font-size: 10px;
        border-bottom: 2px solid var(--navy);
    }}
    
    /* Status Badges */
    .status {{
        font-weight: 700;
        font-size: 10px;
    }}
    .status.alert {{ color: var(--alert-red); }}
    .status.watch, .status.perm {{ color: var(--watch-orange); }}
    .status.ok, .status.intact, .status.thesis-plus {{ color: var(--ok-green); }}
    .status.trimmed {{ color: #555; }}
    
    /* Regime Grid */
    .regime-grid {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        margin-bottom: 10px;
        text-align: center;
    }}
    .regime-card {{
        background-color: white;
        border: 1px solid var(--light-gray);
        padding: 10px;
    }}
    .regime-card .title {{ font-size: 10px; font-weight: bold; color: var(--navy); margin-bottom: 5px; }}
    .regime-card .value {{ font-family: 'Merriweather', serif; font-size: 14px; font-weight: bold; color: var(--navy); white-space: pre-line; line-height: 1.2; }}
    
    .macro-text {{
        font-size: 10px;
        margin-bottom: 30px;
        white-space: pre-wrap;
    }}
    
    /* Macro Grid 8 */
    .macro-grid-8 {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 30px;
    }}
    .macro-card {{
        background-color: white;
        border: 1px solid var(--light-gray);
        border-top: 3px solid var(--gold);
        padding: 12px 10px;
    }}
    .macro-card .title {{ font-size: 10px; font-weight: bold; color: var(--navy); margin-bottom: 5px; }}
    .macro-card .value {{ font-family: 'Merriweather', serif; font-size: 14px; font-weight: bold; margin-bottom: 5px; }}
    .macro-card .sub {{ font-size: 9px; color: #555; line-height: 1.3; }}
    .positive {{ color: var(--ok-green); }}
    .negative {{ color: var(--alert-red); }}
    
    /* Sleeve Grid */
    .sleeve-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr 2fr 2fr;
        gap: 10px;
        margin-bottom: 30px;
    }}
    .sleeve-card {{
        background-color: white;
        border: 1px solid var(--light-gray);
        padding: 10px;
        border-top: 3px solid var(--navy);
    }}
    .sleeve-card.wide {{ grid-column: span 2; }}
    .sleeve-card .title {{ font-size: 12px; font-weight: bold; color: var(--navy); margin-bottom: 5px; }}
    .sleeve-card .weight {{ font-family: 'Merriweather', serif; font-size: 16px; font-weight: bold; margin-bottom: 5px; }}
    .sleeve-card .desc {{ font-size: 9px; color: #555; line-height: 1.3; }}
    
    /* Module Grid */
    .module-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 30px;
    }}
    .module-card {{
        background-color: white;
        border: 1px solid var(--light-gray);
        padding: 12px;
        border-top: 2px solid var(--navy);
    }}
    .module-card h4 {{ margin: 0 0 5px 0; color: var(--navy); font-size: 11px; text-transform: uppercase; }}
    .module-card .sub-label {{ font-family: 'Merriweather', serif; font-weight: bold; font-size: 14px; margin-bottom: 8px; color: var(--navy); }}
    .module-card p {{ margin: 0; font-size: 10px; color: #444; }}
    
    /* Lists */
    .alert-item {{
        margin-bottom: 15px;
        padding-left: 10px;
        border-left: 3px solid var(--navy);
    }}
    .alert-item strong {{ font-family: 'Merriweather', serif; color: var(--navy); font-size: 11px; }}
    
    .decision-item {{
        margin-bottom: 12px;
    }}
    
    .footer {{
        margin-top: 40px;
        padding-top: 15px;
        border-top: 1px solid var(--gold);
        font-size: 9px;
        color: #777;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
</style>
</head>
<body>

<div class="container">

    <div class="masthead-top">
        <span>ACHELION ARMS &middot; Daily Monitor &middot; April 8, 2026 &middot; CEASEFIRE CONFIRMED &middot; CONFIDENTIAL &mdash; GP Distribution</span>
        <span>CRASH &rarr; DEFENSIVE &middot; Score ~0.72 &middot; Queue WATCH</span>
    </div>

    <div class="masthead">
        <div class="masthead-left">
            <h1>ACHELION ARMS &mdash; Daily Monitor</h1>
            <p>{view.report_date} &middot; {view.quarter_day} &middot; {view.architecture_version}</p>
            <p style="color: var(--navy); margin-top: 5px;"><strong>{view.operator_context}</strong></p>
        </div>
        <div class="masthead-right">
            <div class="regime-title">R E G I M E</div>
            <div class="regime-value">{view.regime_transition}</div>
            <div class="regime-score">Score est. {view.regime_score_str}</div>
            <div class="regime-title" style="margin-top: 5px; color: white; letter-spacing: 0;">{view.regime_sub_status}</div>
        </div>
    </div>

    <div class="session-headline">
        <strong>{view.session_headline.split(' \u2014 ')[0]} &mdash; </strong> {view.session_headline.split(' \u2014 ')[1] if ' \u2014 ' in view.session_headline else view.session_headline}
    </div>

    <h2>1 &middot; MACRO COMPASS &mdash; REGIME SCORING</h2>
    <div class="regime-grid">
        <div class="regime-card"><div class="title">Prior Score</div><div class="value">{view.prior_score}</div></div>
        <div class="regime-card"><div class="title">Current Score</div><div class="value">{view.current_score}</div></div>
        <div class="regime-card"><div class="title">Score Change</div><div class="value">{view.score_change}</div></div>
        <div class="regime-card"><div class="title">Queue Trigger</div><div class="value">{view.queue_trigger}</div></div>
        <div class="regime-card"><div class="title">Equity Ceiling</div><div class="value">{view.equity_ceiling}</div></div>
    </div>
    <div class="macro-text">
        {view.macro_drivers_text}
        
        <strong>Score key:</strong> RISK_ON &le;0.30 &middot; WATCH 0.31&ndash;0.50 &middot; NEUTRAL 0.51&ndash;0.65 &middot; DEFENSIVE 0.66&ndash;0.80 &middot; CRASH >0.80
    </div>

    <h2>2 &middot; MACRO INPUTS &mdash; WEDNESDAY MORNING</h2>
    {macro_grid_html}

    <h2>3 &middot; EQUITY BOOK &mdash; CRASH CEILING LIFTING &middot; BROAD RELIEF RALLY</h2>
    <table>
        <tr><th>Ticker</th><th>Name</th><th>Wt.</th><th>Premkt</th><th>Status</th><th>Flag</th></tr>
        {equity_rows}
    </table>

    <h2>4 &middot; DEPLOYMENT QUEUE &mdash; WATCH STATE ACTIVE &middot; SCORE ~0.72 &middot; 7 POINTS FROM NEUTRAL TRIGGER</h2>
    <table>
        <tr><th style="width: 20px;">#</th><th>Ticker</th><th>Target</th><th>Execution Instruction</th><th>Trigger</th></tr>
        {queue_rows}
    </table>

    <h2>5 &middot; DEFENSIVE SLEEVE + PTRH + CASH</h2>
    <div class="sleeve-grid">
        <div class="sleeve-card"><div class="title">SGOV</div><div class="weight">{view.sleeve_sgov}</div><div class="desc">5-week role complete &middot; Stable &middot; Holds position</div></div>
        <div class="sleeve-card"><div class="title">SGOL</div><div class="weight">{view.sleeve_sgol}</div><div class="desc">Gold +2.5% to $4,820 &middot; Dollar weakening &middot; Retains value</div></div>
        <div class="sleeve-card"><div class="title">DBMF</div><div class="weight">{view.sleeve_dbmf}</div><div class="desc">Oil REVERSAL &middot; &ndash;14% Brent &middot; Monitor for trend signal unwind &middot; URGENT WATCH</div></div>
        <div class="sleeve-card"><div class="title">STRC</div><div class="weight">{view.sleeve_strc}</div><div class="desc">11.5% yield &middot; Pre-deployment watch &middot; Unlocks at NEUTRAL</div></div>
        <div class="sleeve-card wide"><div class="title">PTRH &mdash; {view.ptrh_status_str.split(' (')[0]}</div><div class="desc">DEFENSIVE transition reduces to 1.5&times; &middot; CAM recalculating with Brent $94 &middot; Confirm DTE &ge; 30 on all contracts</div></div>
        <div class="sleeve-card wide"><div class="title">Cash &mdash; {view.cash_weight}</div><div class="weight" style="font-size:12px; font-family:'Open Sans', sans-serif;">Fully intact</div><div class="desc">1.2% core hedge &middot; 2.0% STRC pre-deployment watch &middot; 4.8% ops buffer &middot; Deployment possible this week</div></div>
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
        Data sourced from public markets &middot; Wednesday, April 8, 2026 &middot; Q2 &middot; CEASEFIRE CONFIRMED &middot; Regime: CRASH &rarr; DEFENSIVE ~0.72 &middot; Queue: WATCH STATE &middot; Islamabad Friday &middot; Architecture AB v4.0 &middot; Achelion Capital Management, LLC &middot; CONFIDENTIAL &mdash; For GP and Development Use Only
    </div>

</div>
</body>
</html>
"""
    return html
