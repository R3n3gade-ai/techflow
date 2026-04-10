import json
import os
import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.reporting.daily_monitor import run_daily_monitor

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def run():
    print("Loading organic data from state files...")
    snapshot = load_json('data/mj_portfolio_snapshot.json')
    pm_notes = load_json('data/mj_pm_notes.json')
    
    equity_book = []
    for ticker, info in snapshot.get('equities', {}).items():
        equity_book.append({
            'ticker': ticker,
            'name': ticker,
            'weight': info.get('weight', 0.0),
            'session_perf': 0.0,
            'status': info.get('status', 'OK'),
            'rationale': info.get('flag', '')
        })
        
    defensive_sleeve = []
    for ticker, weight in snapshot.get('defensive_sleeve', {}).items():
        defensive_sleeve.append({
            'ticker': ticker,
            'weight': weight,
            'rationale': 'ACTIVE'
        })
        
    raw_inputs = {
        'nav': snapshot.get('nav', 0.0),
        'score': 0.72,
        'score_direction': '↓',
        'queue_status': 'WATCH',
        'macro_compass_score_yesterday': 0.85,
        'macro_compass_trigger': 0.65,
        'macro_compass_next_catalyst': 'Islamabad talks Friday',
        'macro_compass_drivers_up': 'Geopolitical resolution, Rate cut bets',
        'macro_compass_drivers_down': 'Temporary ceasefire expiry risk',
        'macro_inputs': {
            'VIX': {'value': pm_notes.get('macro_cards', {}).get('vix', {}).get('value', '20-22'), 'context': pm_notes.get('macro_cards', {}).get('vix', {}).get('sub', '')},
            'BRENT': {'value': pm_notes.get('macro_cards', {}).get('brent', {}).get('value', '$94'), 'context': pm_notes.get('macro_cards', {}).get('brent', {}).get('sub', '')},
            'SP500': {'value': pm_notes.get('macro_cards', {}).get('sp500', {}).get('value', '+2.5%'), 'context': pm_notes.get('macro_cards', {}).get('sp500', {}).get('sub', '')}
        },
        'equity_book': equity_book,
        'deployment_queue': [],
        'defensive_sleeve': defensive_sleeve,
        'module_status': {
            'PTRH': {'status': 'ACTIVE', 'detail': f"Multiplier {snapshot.get('ptrh_multiplier', 1.0)}x"},
            'ARES': {'status': 'WATCH', 'detail': "Queue WATCH"},
            'DSHP': {'status': 'MONITOR', 'detail': "Monitoring DBMF"}
        }
    }
    
    market_context = json.dumps(pm_notes)
    
    print("Synthesizing Daily Monitor using Gemini 3.1 Pro...")
    markdown_output = run_daily_monitor(raw_inputs, market_context)
    
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    out_path = f"achelion_arms/logs/daily_monitor_organic_{date_str}.md"
    with open(out_path, "w") as f:
        f.write(markdown_output)
        
    print(f"Daily Monitor successfully generated at: {out_path}")

if __name__ == "__main__":
    run()
