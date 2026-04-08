#!/bin/bash
# Wrapper to run the ARMS backtest for a specific year
YEAR=$1
if [ -z "$YEAR" ]; then
    echo "Usage: ./simulate.sh YYYY"
    echo "Example: ./simulate.sh 2020"
    exit 1
fi

echo "Initiating ARMS Phase 1 Backtest for $YEAR..."
python3 -c "from src.simulation.historical_engine import run_simulation; from src.simulation.tearsheet import generate_tearsheet; res = run_simulation('${YEAR}-01-01', '${YEAR}-12-31'); generate_tearsheet(res.history, '${YEAR}-01-01', '${YEAR}-12-31', 50_000_000.0)"
