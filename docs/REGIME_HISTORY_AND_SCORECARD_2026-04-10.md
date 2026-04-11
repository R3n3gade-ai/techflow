# Regime History and Weekly Scorecard — 2026-04-10

## What changed
ARMS now persists regime-score history to:
- `achelion_arms/state/regime_history.json`

Each cycle appends:
- timestamp
- score
- regime
- effective equity ceiling
- queue status
- catalyst label
- short note

The Daily Monitor now uses this durable history to:
- derive `prior_score`
- render a `RECENT REGIME HISTORY` section

## Why this matters
Before:
- prior score was rough/scaffolded
- weekly scorecard did not exist as durable state

After:
- prior score comes from stored regime history when available
- the monitor can start reflecting recent regime evolution instead of inventing a prior comparison

## Remaining gaps
1. history entries are still cycle-based, not fully session/market-session normalized
2. the weekly scorecard is still minimal and should eventually include richer market summary data
3. session/weekly performance still needs real sourced returns
