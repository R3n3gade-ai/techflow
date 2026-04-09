#!/bin/bash
# Wrapper to run the ARMS backtest for a specific year
YEAR=$1
PHASE=${2:-2}

if [ -z "$YEAR" ]; then
    echo "Usage: ./simulate.sh YYYY [PHASE]"
    echo "Example: ./simulate.sh 2020 2"
    exit 1
fi

echo "Initiating ARMS Phase $PHASE Backtest for $YEAR..."

if [ "$PHASE" == "1" ]; then
    python3 -c "from src.simulation.historical_engine import run_simulation; from src.simulation.tearsheet import generate_tearsheet; res = run_simulation('${YEAR}-01-01', '${YEAR}-12-31'); generate_tearsheet(res.history, '${YEAR}-01-01', '${YEAR}-12-31', 50_000_000.0, 1)"
else
    python3 -c "from src.simulation.historical_engine_phase2 import run_simulation_phase2; from src.simulation.tearsheet import generate_tearsheet; res = run_simulation_phase2('${YEAR}-01-01', '${YEAR}-12-31'); generate_tearsheet(res.history, '${YEAR}-01-01', '${YEAR}-12-31', 50_000_000.0, 2)"
fi
