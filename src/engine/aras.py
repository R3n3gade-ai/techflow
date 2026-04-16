"""
ARMS Engine: ARAS Composite Risk Assessor (L3)

The highest authority on gross portfolio exposure. Consumes the 
Macro Compass score and applies the canonical equity ceiling limits.

EDR Advisory Integration (Addendum 7/8):
  Deleveraging Risk and Crypto Microstructure sub-modules provide
  advisory contributions to the composite score. Max individual: +0.06.
  Max dual-module combined: +0.12. Neither module can force a regime
  change independently. Advisory pressure only — never relaxes ceiling.

Canonical thresholds from CLAUDE.md v4.0 (single source of truth):
  Boundaries:  0.30, 0.50, 0.65, 0.80
  Hysteresis:  +0.05 to escalate, -0.05 to de-escalate (10-point band)
  NEUTRAL persistence: 2 consecutive sessions before DEFENSIVE escalation

Reference: CLAUDE.md KEY THRESHOLDS section & REGIME DEFINITIONS table
"""
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ArasOutput:
    regime: str
    score: float
    equity_ceiling_pct: float
    dual_edr_alert: bool = False
    edr_advisory_total: float = 0.0

# ─── Canonical regime definitions (CLAUDE.md v4.0) ───
REGIME_NAMES    = ["RISK_ON", "WATCH", "NEUTRAL", "DEFENSIVE", "CRASH"]
REGIME_CEILINGS = [1.00,      1.00,    0.75,      0.40,        0.15]
REGIME_BOUNDARIES = [0.30, 0.50, 0.65, 0.80]  # 4 boundaries → 5 regimes

# Hysteresis: composite must exceed boundary + HYSTERESIS to escalate,
# or drop below boundary - HYSTERESIS to de-escalate.
# CLAUDE.md: HYSTERESIS_UP = 0.35, HYSTERESIS_DOWN = 0.25
# First boundary 0.30 ± 0.05 = triggers at 0.35 (up) / 0.25 (down)
HYSTERESIS = 0.05

# NEUTRAL persistence: 2 consecutive sessions with confirmed NEUTRAL composite
# before escalating to DEFENSIVE. Prevents single-session pass-through.
NEUTRAL_PERSISTENCE_SESSIONS = 2


def _edr_advisory_contribution(score: float) -> float:
    """
    Per Addendum 7/8 Section 5 contribution table.
    Maps an EDR sub-module score to its advisory contribution.
    Max individual contribution: +0.06.
    """
    if score >= 0.75:
        return 0.06
    if score >= 0.60:
        return 0.04
    if score >= 0.40:
        return 0.02
    return 0.0


class ARASAssessor:
    """
    Stateful ARAS regime assessor with hysteresis and NEUTRAL persistence.

    Three noise-suppression mechanisms (per GP directive):
    1. Hysteresis bands: ±0.05 around each boundary
    2. NEUTRAL persistence: 2-session hold before DEFENSIVE escalation
    3. Single-step transitions per session (except crash jumps)

    EDR advisory contributions (Addendum 7/8 Section 5):
    Sub-module scores add to the composite before regime mapping.
    Dual-module alert fires when both exceed 0.60 simultaneously.
    """

    def __init__(self):
        self._regime_idx = 0  # Start at RISK_ON
        self._neutral_count = 0  # Consecutive sessions at NEUTRAL

    @property
    def current_regime(self) -> str:
        return REGIME_NAMES[self._regime_idx]

    def assess(self, regime_score: float,
               delev_score: float = 0.0,
               micro_score: float = 0.0) -> ArasOutput:
        # ── EDR advisory contributions (Addendum 7/8 Section 5) ──
        delev_advisory = _edr_advisory_contribution(delev_score)
        micro_advisory = _edr_advisory_contribution(micro_score)
        edr_total = delev_advisory + micro_advisory

        # Dual-module alert: both > 0.60 (Addendum 8 Section 5)
        dual_alert = delev_score > 0.60 and micro_score > 0.60
        if dual_alert:
            logger.warning(
                "[ARAS] DUAL EDR ALERT: delev=%.3f micro=%.3f combined_advisory=+%.3f",
                delev_score, micro_score, edr_total
            )

        # Apply advisory pressure (upward only — never relaxes)
        adjusted_score = min(1.0, regime_score + edr_total)

        idx = self._regime_idx

        # ── Try escalation (toward more defensive) ──
        # Allow multi-step jumps (e.g., RISK_ON → CRASH in a flash crash)
        escalated = True
        while escalated and idx < 4:
            escalated = False
            boundary = REGIME_BOUNDARIES[idx]
            if adjusted_score >= boundary + HYSTERESIS:
                # NEUTRAL → DEFENSIVE: persistence gate
                if idx == 2:
                    if self._neutral_count < NEUTRAL_PERSISTENCE_SESSIONS:
                        break  # Block — need more sessions in NEUTRAL
                idx += 1
                escalated = True

        # ── Try de-escalation (toward more aggressive) ──
        # Only if we didn't escalate this session
        if idx == self._regime_idx:
            deescalated = True
            while deescalated and idx > 0:
                deescalated = False
                boundary = REGIME_BOUNDARIES[idx - 1]
                if adjusted_score <= boundary - HYSTERESIS:
                    idx -= 1
                    deescalated = True

        # ── Track NEUTRAL persistence ──
        if idx == 2:
            self._neutral_count += 1
        else:
            self._neutral_count = 0

        self._regime_idx = idx
        return ArasOutput(
            regime=REGIME_NAMES[idx],
            score=adjusted_score,
            equity_ceiling_pct=REGIME_CEILINGS[idx],
            dual_edr_alert=dual_alert,
            edr_advisory_total=edr_total,
        )


def calculate_aras_ceiling(regime_score: float) -> ArasOutput:
    """
    STATELESS regime mapping (backward-compatible).
    Uses canonical GP thresholds but NO hysteresis or persistence.
    For full spec compliance, use ARASAssessor.assess() instead.
    """
    if regime_score < 0.30:
        regime = "RISK_ON"
        ceiling = 1.00
    elif regime_score <= 0.50:
        regime = "WATCH"
        ceiling = 1.00
    elif regime_score <= 0.65:
        regime = "NEUTRAL"
        ceiling = 0.75
    elif regime_score <= 0.80:
        regime = "DEFENSIVE"
        ceiling = 0.40
    else:
        regime = "CRASH"
        ceiling = 0.15

    return ArasOutput(regime=regime, score=regime_score, equity_ceiling_pct=ceiling)
