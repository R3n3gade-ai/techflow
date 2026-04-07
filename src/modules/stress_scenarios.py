"""
ARMS Engine: Stress Scenario Library (SSL)

Runs daily after portfolio snapshot. Applies 8 historical and custom stress 
scenarios to current portfolio weights to estimate P&L.

Reference: THB v4.0, Section 8
"""
from dataclasses import dataclass, field
from typing import List, Dict
import datetime

@dataclass
class ScenarioPnL:
    scenario_id: str
    scenario_name: str
    portfolio_pnl_pct: float
    portfolio_pnl_usd: float
    hedge_offset_usd: float
    net_pnl_after_hedge: float

@dataclass
class ScenarioResults:
    as_of: str
    current_nav: float
    scenarios: List[ScenarioPnL]
    worst_scenario: str
    worst_net_loss_pct: float

# Hardcoded shock matrices from THB v4.0 Section 8.1
# Format: { ScenarioID: { "Name": str, "QQQ_shock": float, "BTC_shock": float, "Defensive_Offsets": dict } }
SCENARIOS = {
    "S1": {"name": "2008 Lehman Collapse", "qqq": -0.35, "btc": -0.35, "offsets": {"SGOL": 0.12, "SGOV": 0.05}},
    "S2": {"name": "2020 COVID Crash", "qqq": -0.34, "btc": -0.53, "offsets": {"SGOV": 0.03}},
    "S3": {"name": "2022 Rate Shock", "qqq": -0.22, "btc": -0.35, "offsets": {"SGOV": -0.05, "DBMF": 0.08}},
    "S4": {"name": "Flash Crash — Intraday", "qqq": -0.10, "btc": -0.15, "offsets": {}},
    "S5": {"name": "Hormuz Closed 90 Days", "qqq": -0.15, "btc": -0.10, "offsets": {"SGOL": 0.18, "DBMF": 0.12}},
    "S6": {"name": "Crypto Bear", "qqq": 0.0, "btc": -0.60, "offsets": {}},
    "S7": {"name": "Fed Shock +100bps", "qqq": -0.12, "btc": -0.20, "offsets": {"SGOV": 0.01}},
    "S8": {"name": "AI Bubble Unwind", "qqq": -0.40, "btc": -0.20, "offsets": {"SGOL": 0.08}}
}

def run_stress_scenarios(nav: float, portfolio_weights: Dict[str, float], ptrh_notional: float) -> ScenarioResults:
    """
    Applies the 8 scenarios to the current portfolio weights and PTRH hedge.
    """
    results = []
    worst_scenario_id = "S1"
    worst_net_loss = 0.0

    for sid, data in SCENARIOS.items():
        # Simplistic calculation: Assume all equity correlates 1:1 to QQQ in shock for demo
        # Assume specific crypto tickers correlate 1:1 to BTC shock
        equity_weight = sum(w for t, w in portfolio_weights.items() if t not in ['IBIT', 'ETHB', 'BSOL', 'SGOL', 'DBMF', 'SGOV'])
        crypto_weight = sum(w for t, w in portfolio_weights.items() if t in ['IBIT', 'ETHB', 'BSOL'])
        
        equity_pnl_pct = equity_weight * data["qqq"]
        crypto_pnl_pct = crypto_weight * data["btc"]
        
        defense_pnl_pct = 0.0
        for def_ticker, shock in data["offsets"].items():
            if def_ticker in portfolio_weights:
                defense_pnl_pct += portfolio_weights[def_ticker] * shock

        gross_pnl_pct = equity_pnl_pct + crypto_pnl_pct + defense_pnl_pct
        gross_pnl_usd = gross_pnl_pct * nav

        # PTRH Offset Estimation (Delta -0.35 approximation in deep shock)
        # Simplified: If QQQ drops X%, Put gains ~ (-delta * X * notional * convexity_factor)
        # For a hard crash (-30%), the hedge pays out aggressively.
        hedge_offset_usd = 0.0
        if data["qqq"] < 0:
            # Rough convexity approximation for deep OTM puts
            convexity_mult = 1.5 if data["qqq"] < -0.20 else 1.0
            hedge_offset_usd = abs(data["qqq"]) * ptrh_notional * 0.35 * convexity_mult

        net_usd = gross_pnl_usd + hedge_offset_usd
        net_pct = net_usd / nav if nav > 0 else 0.0

        if net_pct < worst_net_loss:
            worst_net_loss = net_pct
            worst_scenario_id = sid

        results.append(ScenarioPnL(
            scenario_id=sid,
            scenario_name=data["name"],
            portfolio_pnl_pct=gross_pnl_pct,
            portfolio_pnl_usd=gross_pnl_usd,
            hedge_offset_usd=hedge_offset_usd,
            net_pnl_after_hedge=net_usd
        ))

    return ScenarioResults(
        as_of=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        current_nav=nav,
        scenarios=results,
        worst_scenario=worst_scenario_id,
        worst_net_loss_pct=worst_net_loss
    )
