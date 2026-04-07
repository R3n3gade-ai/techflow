# Addendum 6: PTRH Adaptive Strike Protocol
Delta-Primary Architecture | Autonomous Fallback Resolution | Self-Calibrating Drift Detection

3. Autonomous Fallback Resolution Hierarchy
The prior specification produced a binary outcome: compliant or abort. Abort was appropriate for discretionary
trades where discipline is the primary objective. It is not appropriate for essential portfolio infrastructure where tail
protection continuity is the primary objective.
ARMS will now work through a four-gate fallback hierarchy autonomously before generating a no-execute
condition. Each fallback level relaxes outer boundaries while preserving the governing intent. All fallback
executions are logged with the specific fallback level invoked and the reason Gate 1 was unavailable.

Gate Delta DTE OTM Guardrail Spread Log & Notification
1 — STANDARD -0.30 to -0.40 60 to 90 days 2% to 10% <= 5% Standard execution log. No alert.
2 — RELAXED -0.28 to -0.42 55 to 95 days 1.5% to 12% <= 7% Log: FALLBACK-2. Queue ARMS Architecture Review flag. PM notification deferred (next daily summary).
3 — EXTENDED -0.25 to -0.45 45 to 105 days 1% to 15% <= 10% Log: FALLBACK-3. Generate PTRH-SPEC-DRIFT alert with market snapshot. PM notification: immediate.
4 — ABORT No contract satisfies Gate 3 Log: PTRH-NO-EXECUTE with full market conditions snapshot. PM immediate alert. Set 24-hour rescan timer. PTRH budget preserved in cash sleeve.
