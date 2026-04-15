"""Quick crypto allocation diagnostic."""
from simulation.historical_engine_phase2 import run_simulation_phase2

res = run_simulation_phase2("2024-01-02", "2026-04-11", initial_capital=500_000_000)
h = res.history

monthly = h.resample("ME").last()
print(f"{'Month':11s} {'Crypto':>7s} {'Equity':>7s} {'Def':>7s} {'Cash':>7s} {'Regime':10s} {'PDS':12s}")
for idx, row in monthly.iterrows():
    m = idx.strftime("%b %Y")
    cr = row["Crypto_Pct"] * 100
    eq = row["Equity_Pct"] * 100
    df = row["Defensive_Pct"] * 100
    ca = row["Cash_Pct"] * 100
    rg = row["Regime"]
    pd = row["PDS_Status"]
    print(f"{m:11s} {cr:6.1f}% {eq:6.1f}% {df:6.1f}% {ca:6.1f}% {rg:10s} {pd}")

# Check if any crypto trims happened
trims = [t for t in res.trade_ledger if t.get("Ticker") == "BTC"]
print(f"\nBTC trades: {len(trims)}")
for t in trims[:20]:
    print(f"  {t['Date']} {t['Action']:6s} ${t['Value']:>12,.0f}  {t.get('Trigger','')}")
