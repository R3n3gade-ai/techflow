# Macro Compass Typed Event State — 2026-04-10

## What changed
The old opaque LLM event-overlay path in `macro_compass.py` has been removed from the live regime score path.

A new deterministic interim path now exists:
- `src/data_feeds/macro_event_state.py`
- events are ingested from SEC / RSS / bridge feeds
- those events are mapped into a typed `MacroEventState`
- `calculate_macro_regime_score()` now consumes that typed state directly

## Why this is better
Before:
- live news context was sent into an LLM prompt
- the model inferred hidden stress scores
- the regime engine was not auditable enough

After:
- event contribution is deterministic
- event contribution is sourced from ingested events
- event contribution is inspectable and explainable

## Current limitation
This is still an interim deterministic heuristic layer, not the final institutional event-state engine.
It is better than opaque prompt inference, but it still needs:
1. richer event taxonomy
2. explicit catalyst calendar state
3. better mapping of diplomacy improvement vs deterioration
4. integration into monitor narrative with typed rationale
