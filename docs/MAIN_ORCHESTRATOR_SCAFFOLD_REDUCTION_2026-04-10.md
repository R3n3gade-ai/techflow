# Main Orchestrator Scaffold Reduction — 2026-04-10

## What changed
The `main.py` Daily Monitor input path was reduced further away from pure placeholder text.

### Improvements
- recent session log is now summarized for report context
- macro cards now include typed event overlay score
- equity book rationale now includes live MICS score
- module panels now expose more actual system metrics
- PM decision queue now reflects live queue/TDC/execution context rather than remediation-only text
- prior score now attempts to use recent log context before falling back to a rough proxy

## Still not finished
This is not full institutional parity yet.
Remaining issues include:
1. prior score history is still weak because session log does not yet persist a clean regime-score timeline
2. session performance is still not truly sourced from market/session returns
3. weekly scorecard is not yet built from a durable state model
4. some operating context remains rough and needs richer typed catalysts / performance state
