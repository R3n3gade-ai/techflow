# Daily Monitor Governance Upgrade — 2026-04-10

## What changed
The Daily Monitor markdown path can now explicitly render:
- active deployment queue
- removed / downgraded queue items
- monitor-list items
- notes explaining governance reasons

## Why this matters
Before this change, queue governance truth was being flattened into a single deployment table.
That meant the report could not honestly express:
- why names were removed
- why names were held instead of sized up
- which names were being monitored due to thesis pressure

Now the markdown report has explicit sections for:
- `Removed / Downgraded Queue Items`
- `Monitor List`

## Remaining gap
The markdown report now has the structural capacity to show governance truth, but the final quality still depends on:
1. richer queue reasoning
2. richer typed monitor state
3. final renderer modernization if we want full MJ-style layout parity
