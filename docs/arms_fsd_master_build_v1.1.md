> **DUPLICATE** � Canonical version: ARMS_FSD_Master_Build_Document_v1.1.md

ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 1
ACHELION CAPITAL MANAGEMENT, LLC
ARMS FSD
Full Autonomous Operations — Master Build Document
For: Josh (Lead Developer)
Version: 1.1 — March 24, 2026 | Revised: Immediate-Build Frontiers Added
Classification: CONFIDENTIAL — GP and Development Use Only
v1.1 adds Section 11: Five frontiers — what gets built now vs. later. Three frontiers are fully
buildable today at zero incremental cost. Josh starts with Section 11 before anything else.
"Silence is trust in the architecture."
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 2
0. The Mandate
The PM declares intent. ARMS executes everything else.
This document is the complete engineering specification for transitioning ARMS from a dashboard-and-
human-execution system to a fully autonomous decision and execution architecture. Every module
described in PM Playbook v4.0 and THB v4.0 must be connected to a live execution pipeline by the end
of Phase 3.
v1.1 adds Section 11 — the Immediate-Build Frontier specifications. Three of the five long-term
frontiers are fully buildable today using free or low-cost tools with zero rearchitecting required when
expensive upgrades arrive. Josh reads Section 11 before starting Phase 1.
The governing principle: human involvement at the execution layer is not a safety feature. It is latency
and error risk. The only legitimate human touchpoints are thesis seeding via the SENTINEL protocol,
regulated confirmation windows that exist to satisfy fiduciary law, and GP-level strategic override with
documented justification and co-sign. Every other decision is owned by the system.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 3
1. System Architecture Overview
ARMS FSD is a seven-layer autonomous system. Each layer produces typed outputs consumed by the
next. No layer polls for human input except at designated confirmation windows. The system is a
pipeline, not a collection of scripts. Build it that way.
Layer Name Function Outputs to
L1 Data Ingestion Market prices, macro signals,
VIX, yields, options flow.
Feed-agnostic plugin
architecture — free feeds
now, institutional feeds later.
L2 — Macro Compass
L2 Macro Compass Regime scoring composite.
Outputs current regime + RPE
probability distribution of next
transition.
L3 — ARAS
L3 ARAS + v4.0 + v5.0
Modules
FEM, PDS, PTRH, CDF,
VARES, LAEP, SSL, MICS,
RPE, CCM, TRP, AUP, SLA
run after portfolio snapshot.
L4 — Master Engine
L4 Master Engine Portfolio construction. Applies
ceiling, MICS-derived C²
weighting, CCM calibration
factor, decay.
L5 — Order Book
L5 Order Book + LAEP Converts allocation delta to
executable orders.
VWAP/market mode, priority,
slippage budget.
L6 — Execution
L6 Execution API Submits orders to broker.
Confirms fills. Logs all
executions with triggering
module and rationale.
L7 — Audit + Monitor
L7 Audit + Daily Monitor Immutable session log. Daily
monitor 6AM CT. Session Log
Analytics monthly. LP
narrative engine reads from
log.
PM / LPs
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 4
2. Four-Tier Autonomy Framework
Every decision in ARMS is classified into one of four tiers. Tier determines whether the system acts
immediately, waits for a veto window, requires confirmation, or defers entirely to human judgment. No
decision may be reclassified upward without GP documentation.
Tier 0 — Fully Autonomous
Zero human touch. System executes immediately. No override accepted.
Action Trigger Execution
Regime ceiling enforcement (ARAS) Composite crosses regime
threshold
Immediate
PDS DELEVERAGE_1 (−12% HWM) NAV falls 12% from high-
water mark
Immediate — 60%
ceiling
PDS DELEVERAGE_2 (−18% HWM) NAV falls 18% from high-
water mark
Immediate — 30%
ceiling
PTRH roll DTE reaches 30 days on any
QQQ put
Same session
PTRH regime resize Regime transition confirmed
by ARAS
Immediate
SLOF activation / deactivation RISK_ON/WATCH: on.
NEUTRAL: reduce.
DEFENSIVE/CRASH: off
Immediate
CDF weight decay (0.80x at 45d, 0.60x at
90d)
Position underperforms QQQ
by 10pp over 45 consecutive
days
Next open
LAEP mode switch VIX crosses 25 or 45 Immediate
MICS scoring on position initiation Every new position through
SENTINEL
Auto — no PM input
RPE update Every 5 minutes with data
refresh
Continuous
Session Log Analytics Monthly after log compilation 1st of month
SSL daily computation + worst-scenario
alert
Daily after portfolio snapshot Pre-market 5:30AM
Systematic Scan Engine weekly run Every Monday pre-market 6AM CT Monday
Daily monitor generation + delivery Scheduled daily 6:00AM CT
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 5
Tier 1 — Default Execute (PM Veto Window)
System executes unless PM vetoes within defined window. No response = execute. Default
is action, not inaction.
Action Trigger Veto Window
PERM covered call execution Unrealized gain exceeds 30%
on any position
4 hours
ARES re-entry T1 deployment All 4 ARES gates clear +
VARES sizes tranche
2 hours
CDF Day 135 orderly exit Day count hits 135 without
conviction reaffirmation
24 hours
FEM ALERT trim recommendation ALERT (>80%) persists 24h
without PM reaffirmation
24 hours
SENTINEL-approved position initiation All 6 gates pass + regime
NEUTRAL or better
4 hours
Thesis Retirement Protocol execution 180d in book + CDF 0.60x +
bear evidence present
24 hours
NOTE: Confirmation queue must be built with three response options from day one — 'no new
information, execute' (immediate), 'new information present, hold' (opens source declaration form),
'veto with rationale' (written reason required). Time-based windows are the fallback, not the primary
interface. See Section 11.5.
Tier 2 — Confirm Required + GP Co-sign
System recommends. PM confirms. GP co-sign required. No default execution.
Action Why Human Required Window
ARAS regime override PM holds pre-consensus insight the
model cannot encode. Logged
permanently.
GP co-sign
Architecture AB structural
change
Changing 58/20/14/8 requires thesis-level
conviction about civilizational shift
weighting.
Full GP vote
LP communication narrative
approval
Legal and relationship context. Auto-
generated; PM approves before send.
2 hours
MICS override by ±2 or more
levels
Extraordinary circumstance. PM must
document specific rationale.
GP co-sign
Tier 3 — Human Only
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 6
No system recommendation possible. This is where human edge lives and ends.
Thesis seeding Pre-consensus pattern recognition from lived experience.
What is known before it enters any dataset.
LP relationship management Trust, credibility, and emotional intelligence in capital
conversations.
GP strategic vision What Achelion is, what it stands for, where it goes.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 7
3. SENTINEL v2.0 — New Position Protocol
SENTINEL v2.0 introduces three structural upgrades: a quantitative mispricing score at Gate 3, a
mandatory adversarial cross-examination layer, and a source quality taxonomy at Gate 6. The output of
Gates 1–5 feeds directly into the MICS formula — the PM no longer assigns a free conviction level.
# Evaluator Gate Question Standard Fail Condition
1
AI Civilizational
shift — not a
product cycle?
Binary. The test: does this
company exist whether or not any
individual product succeeds? No
hedging. No partial credit.
Fail = rejected. No appeal.
2
AI Non-optional —
cannot be routed
around?
Binary with AI research. Models
substitutability and structural
necessity. 'Potential' does not pass.
Current necessity only.
Fail = rejected.
3
AI +
QUANT
Quantitative
mispricing score
(0–30)
Three factors 0–10 each: multiple
mispricing, institutional positioning
gap, consensus framing gap. Cat
A/B: threshold 14/30. Cat C:
threshold 20/30. Narrative cannot
override the number.
Below threshold = fail. No
override.
4
AI + FEM Architecture AB
fit — no
concentration
without paired
trim?
FEM impact modeled before entry.
WATCH→ALERT: paired trim
required. Already ALERT: blocked.
Mechanical gate.
ALERT worsened =
blocked.
5
AUTO Regime timing —
entry defensible?
RISK_ON/WATCH: proceed.
NEUTRAL: VARES sizing.
DEFENSIVE: queued. CRASH:
blocked. No override.
DEFENSIVE/CRASH =
queued 90 days.
6
PM
SOURCE
Pre-consensus
source
declaration
Source category declared from
taxonomy (Section 4). Feeds MICS
formula as source_score. No
response = Cat 'no PM input' score
(4/10). Cat D not accepted.
Cat D = rejected.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 8
4. Gate 6 Source Quality Taxonomy
The source taxonomy is the mechanism by which free conviction assignment is removed. The PM
declares a category. The category feeds the MICS source_score. Cat D does not exist as an input field
— the system will not accept it.
Category Definition Examples MICS
source_score
Gate 3
threshold
Cat A
Primary
source
Direct conversation
with founder,
engineer, customer,
or supply chain
participant with
firsthand knowledge
not yet public.
TSMC supply chain VP
describing capacity
allocation. Hyperscaler
engineer on internal tooling.
Founder explaining structural
advantage before public
announcement.
10 / 10 14 / 30
Cat B
Pattern
recognition
PM has seen this
exact configuration
before in a prior cycle.
Structural analog is
clear. Pattern not yet
in consensus.
NVDA 2020 rhymes with
Cisco 1996. TSLA energy/AI
thesis before auto framing
dissolved. 28 years of cycle
recognition applied to current
setup.
8 / 10 14 / 30
Cat C
Synthesis
Synthesis of public
information not yet at
consensus framing.
PM connected dots
the market has not yet
connected.
Five earnings call transcripts
revealing a supply chain shift
no analyst has framed.
Macro data connected to
sector implication absent
from Street research.
5 / 10 20 / 30
No PM
input
(silence)
PM has no pre-
consensus insight to
add beyond what the
system already
knows. Silence is trust
in the architecture.
System executes at
MICS-implied sizing.
4-hour veto window expires
with no PM response. MICS
uses source_score of 4/10
— system proceeds at
reduced conviction relative to
Cat A/B. This is a valid and
expected outcome.
4 / 10
Gate 3
threshold
still applies
Cat D Does
not exist
Strong opinion. Gut
feeling. Conviction
without identifiable
source. Not a
category. Not an input
field. The steering
wheel we removed.
Every rationalization a PM
has made while overriding a
risk system. The entire
history of human error in
portfolio management
compressed into one
category the system will not
accept.
REJECTED REJECTED
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 9
5. Five New Modules — Sharpening the Weapon
These five modules extend ARMS into anticipation, self-calibration, symmetric upside capture,
proactive LP trust-building, and thesis retirement. Build status for each is specified in Section 11.
5.1 Regime Probability Engine (RPE)
From reactive to anticipatory. Pre-position before transitions rather than react to them.
File src/engine/regime_probability.py
Runs Every 5 minutes with data ingestion cycle
Build status Phase 1 — see Section 11.1
Feeds into ARAS advisory, PTRH sizing, SLOF margin, cash
accumulation
5.2 Conviction Calibration Module (CCM)
Self-correcting conviction scoring. The PM who calls it right gets amplified. Noise gets
corrected.
File src/engine/conviction_calibration.py
Runs Quarterly after session log compilation
Build status Phase 2 — requires 90 days of session log data
Feeds into Master Engine conviction_weighting_factor
5.3 Thesis Retirement Protocol (TRP)
Exit with the same rigor SENTINEL applies to entry.
File src/engine/thesis_retirement.py
Trigger 180d in book + CDF at 0.60x + bear case evidence present in
current data
Build status Phase 2
Feeds into PERM exit queue (Tier 1 default-execute)
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 10
5.4 Proactive Intelligence Digest (PID)
Transparency as competitive advantage. The LP who sees the system working every month
never redeems.
File src/reporting/proactive_digest.py
Frequency Monthly — automated
Build status Phase 3
Contents Current regime + scoring · Top 3 SENTINEL analyses · SSL
worst-scenario vs. prior month
5.5 Asymmetric Upside Protocol (AUP)
ARMS is currently built to protect capital. AUP makes it equally precise at compounding it.
File src/engine/asymmetric_upside.py
Trigger All 5 conditions: RISK_ON + avg conviction >7.5 + FEM clean
+ RPE <20% WATCH prob + SSL net loss <12%
Build status Phase 2
Output Tier 1 SLOF expansion + conviction upgrade
recommendations
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 11
6. Build Roadmap — Three Phases to Full FSD
Section 11 expands Phase 1 with the immediate-build frontier specifications. Read Section 11 first, then
return here for the full phase context.
Phase Timeline Core Deliverables Milestone
Phase 1
Months
1–2 1. MICS formula — 2-3 days. Highest priority
inch. See Section 11.1.
2. Feed-agnostic data ingestion pipeline with
free feeds. See Section 11.2.
3. Systematic Scan Engine (~$150/month
Claude API). See Section 11.3.
4. Session Log Analytics module. See Section
11.4.
5. Confirmation queue with information-quality
response options. See Section 11.5.
6. Brokerage API integration (IBKR/Alpaca). Tier
0 execution live.
7. RPE (Module 5.1) — continuous regime
probability scoring.
Tier 0 fully live. MICS
replaces PM conviction
assignment. Three
frontiers closed. Feed
receptors built. ARMS
begins flying itself.
Phase 2
Months
3–4 1. SENTINEL engine as automated module. Full
6-gate analysis on PM thesis seed.
2. CCM (Module 5.2) — quarterly conviction
calibration. Requires 90 days of session log.
3. TRP (Module 5.3) — thesis retirement
protocol.
4. AUP (Module 5.5) — asymmetric upside
protocol.
5. Model Optimization Engine — quarterly
parameter review from session log.
Tier 1 default-execute
live. SENTINEL fully
automated. Entry and exit
equally rigorous. System
begins self-calibrating.
Phase 3
Months
5–6 1. PID (Module 5.4) — monthly automated LP
report.
2. Full audit infrastructure — immutable session
log, regulatory compliance layer.
3. Performance attribution by module.
4. Aggregate Signal Monitor for multi-portfolio
and licensing instances.
5. ARMS licensing config layer — fund-agnostic
parameter set. ARMS becomes a platform.
Full FSD. Every decision
defensible. ARMS is a
licensable product.
Achelion is a platform.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 12
7. Updated File Structure — v5.0 Target
New files are marked NEW. Modified files are marked UPDATED. Unchanged v4.0 files are marked
UNCHANGED.
File Status Description
src/data_feeds/market_data.py
UPDATED
Feed-agnostic plugin architecture.
Free feeds now; institutional
feeds plug in later without rebuild.
src/data_feeds/free_signals.py
NEW
SEC EDGAR, FRED, USPTO,
Quiver Quantitative, Adzuna job
data. Phase 1 free signal layer.
src/engine/regime_probability.py
NEW
Regime Probability Engine. Every
5 min. Outputs
RegimeProbabilitySignal.
src/engine/macro_compass.py UNCHANGED Core regime detection.
Unchanged from v4.0.
src/engine/aras.py UPDATED Consumes RPE advisory signal.
Pre-positioning logic added.
src/engine/master_engine.py
UPDATED
Consumes MICS score and CCM
calibration factor. C² weighting
derived from MICS.
src/engine/mics.py
NEW
Model-Implied Conviction Score
formula. 2-3 days to build. Phase
1 priority #1.
src/engine/conviction_calibration.py
NEW
CCM. Runs quarterly. Outputs
calibration factor. Phase 2 —
needs 90d of log data.
src/engine/thesis_retirement.py
NEW
Thesis Retirement Protocol. 3-
condition trigger. Queues orderly
exit. Phase 2.
src/engine/asymmetric_upside.py NEW Asymmetric Upside Protocol. 5-
condition trigger. Phase 2.
src/engine/session_log_analytics.py
NEW
Monthly log analysis. Three
output metrics. Phase 1 —
learning loop receptor.
src/engine/systematic_scan.py
NEW
Weekly SENTINEL scan of AI
infrastructure universe. Claude
API ~$150/month. Phase 1.
src/engine/kevlar.py UNCHANGED Position limits. Unchanged from
v4.0.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 13
src/engine/perm.py UPDATED Connected to TRP for thesis
retirement exits.
src/engine/slof.py UPDATED AUP expansion eligibility check
added.
src/engine/ares.py UNCHANGED VARES re-entry sizing.
Unchanged from v4.0.
src/engine/drawdown_sentinel.py UNCHANGED PDS. Unchanged from v4.0.
src/engine/tail_hedge.py
UPDATED
Consumes RPE pre-positioning
signals for PTRH sizing ahead of
regime transitions.
src/modules/factor_exposure.py UNCHANGED FEM. Unchanged from v4.0.
src/modules/stress_scenarios.py UNCHANGED SSL. Unchanged from v4.0.
src/execution/broker_api.py NEW Brokerage API (IBKR/Alpaca).
Phase 1 priority #2 after MICS.
src/execution/confirmation_queue.py
NEW
Tier 1 veto windows with 3-option
information-quality interface.
Phase 1.
src/execution/sentinel_engine.py NEW SENTINEL v2.0 as automated
module. Phase 2.
src/execution/order_book.py UNCHANGED LAEP execution. Unchanged from
v4.0.
src/reporting/daily_monitor.py UPDATED Auto-generates full monitor 6AM
CT. All v4.0 + v5.0 module status.
src/reporting/proactive_digest.py NEW PID monthly automated LP report.
Phase 3.
src/reporting/audit_log.py
NEW
Immutable session log. Every
action timestamped with module
source. Phase 1.
src/reporting/session_log_analytics.py NEW Monthly learning loop metrics.
Phase 1.
src/reporting/performance_attribution.py NEW Module-level attribution. Phase 3.
src/api/dashboard_api.py
UPDATED
Exposes all new module outputs
including MICS, RPE, SLA, scan
results.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 14
8. Phase 1 Sprint — Josh's First Two Months
Read Section 11 before this section. Three of the five build items below are expanded with
full specifications in Section 11.
Phase 1 has two non-negotiable priorities in order: (1) MICS — closes the conviction assignment
problem immediately, zero new APIs required; (2) brokerage API integration — closes the gap between
signal and execution. Everything else follows.
8.1 Priority Sequence for Phase 1
1. MICS formula (src/engine/mics.py). 2-3 days. Full spec in Section 11.1. Build this first.
2. Feed-agnostic data ingestion pipeline with free signal plugins (src/data_feeds/). 1 week. Full
spec in Section 11.2.
3. Systematic Scan Engine (src/engine/systematic_scan.py). 2 weeks. Full spec in Section 11.3.
~$150/month Claude API.
4. Session Log Analytics (src/engine/session_log_analytics.py). 1 day. Full spec in Section 11.4.
5. Confirmation queue with information-quality response options
(src/execution/confirmation_queue.py). Full spec in Section 11.5.
6. Brokerage API integration (src/execution/broker_api.py). IBKR via ib_insync. See Section 8.2.
7. Regime Probability Engine (src/engine/regime_probability.py). Module 5.1.
8.2 Brokerage API Integration
Recommended: Interactive Brokers (IBKR) via the ib_insync Python library. Preferred for institutional
use — deeper options support for PTRH, better fill quality, cleaner audit trail for regulatory purposes.
Alpaca is acceptable as a simpler REST-based alternative for initial testing.
Minimum viable connection for Phase 1
8. Account connection and position snapshot. ARMS reads live portfolio to calculate allocation
deltas.
9. Order submission (market and VWAP). LAEP mode determines which type fires.
10. Fill confirmation and logging. Every executed order writes to audit log with triggering module.
11. Options order support. PTRH put positions require options chain access and spread capability.
8.3 The OrderRequest Interface — Freeze Before Connecting
Every ARMS module that triggers a trade produces an OrderRequest. The order book consumes
OrderRequest objects regardless of which module produced them. This interface must be defined and
frozen before any module connects to execution.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 15
@dataclass class OrderRequest:
ticker: str
action: Literal['BUY','SELL','BUY_PUT','SELL_CALL']
quantity: int
order_type: str # 'MARKET' | 'VWAP' | 'LIMIT'
execution_window_min: int # from LAEP mode
slippage_budget_bps: float # from LAEP mode
priority: int # 1-4 kill chain order
triggering_module: str # 'ARAS'|'PDS'|'PTRH'|'MICS'|etc.
triggering_signal: str # human-readable rationale
tier: int # 0=immediate, 1=veto window
veto_window_hours: float # 0 for Tier 0
confirmation_required: bool
8.4 Testing Protocol Before Live Connection
12. Paper trading mode. Connect to IBKR paper account. Run full system 30 days. Every order
logged and manually verified. No discrepancies before proceeding.
13. Regime transition test. Force Macro Compass composite from RISK_ON through CRASH and
back. Verify every module fires in correct sequence at correct ceiling.
14. Kill chain test. Force PDS DELEVERAGE_1 in paper mode. Verify kill chain executes to 60%
ceiling with correct priority order. Verify audit log captures every order.
8.5 Day One Checklist for Josh
• Read PM Playbook v4.0 and THB v4.0 in full. Both are canonical. No prior version is relevant.
• Read Section 11 of this document before writing any code.
• Review Architecture AB canonical weights and the five-regime ceiling table.
• Set up IBKR paper account. Obtain API credentials.
• Install ib_insync. Confirm connection to paper account from dev environment.
• Read the existing ARMS codebase zip files from MJ. Map every module to the Layer diagram in
Section 1.
• Define and freeze the OrderRequest interface (Section 8.3) before connecting anything to
execution.
• Build src/engine/mics.py first. Two to three days. This is the highest-value inch available.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 16
9. The LP Narrative
"Most funds tell you they have a disciplined process. We have removed the human from the
process entirely — except where human judgment is genuinely irreplaceable."
What most funds say We have a disciplined investment process managed by an
experienced team.
What Achelion says We have removed the human from the execution process
entirely. Our PM does one thing no algorithm can replicate: he
identifies what the world will look like before the data confirms
it. Everything after that is engineering.
What this means for LPs You are not betting on our judgment in a crisis. You are
betting on an architecture that was designed specifically for
the crisis you have not seen yet.
How we prove it The session log is immutable. Every decision has a
timestamp, a triggering signal, and the module that generated
it. You can verify the system ran exactly as described in every
single session.
The Buffett correction Far more money has been lost on Wall Street by salesmen
than by investors. ARMS removes the curtain entirely. Judge
us on the process, not the narrative.
On MICS specifically Our conviction scoring is not assigned by a portfolio manager.
It is derived from a quantitative formula applied to the same
gate data that governs every entry decision. The PM can
adjust it by one level with a documented reason. That is the
entire scope of human involvement in sizing.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 17
10. Closing Statement
The factory is built. The robots are ready. The humans are in the control room.
What follows from the completion of this build is not an incremental improvement to how Achelion
manages capital. It is a categorical change in what a hedge fund can be.
For the first time at the emerging fund level, a portfolio will be managed by a system that detects
regime transitions before they happen, scores conviction from data rather than opinion, executes
without emotional interference, and gets smarter over time through calibration and thesis retirement
feedback loops — while a human partner brings the one thing no system can replicate: the ability to see
the future before it is in the data.
The best version of human judgment is not a human trying to outperform a machine in the machine's
domain. It is a human working with a machine in a partnership where each does what it does best —
and neither pretends to do the other's job.
"Silence is trust in the architecture."
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 18
11. Immediate-Build Frontiers — What Josh Builds Now
Inches today, miles later. Every receptor built now accepts the expensive upgrade without
rearchitecting. This section is Josh's first read.
Of the five long-term frontiers identified in the strategic architecture review, three are fully buildable
today at zero or near-zero incremental cost. Two require expensive data feeds or infrastructure not yet
justified by current AUM — but their receptors must be built now so the upgrades are configuration
changes, not rebuilds.
Frontier Build now? Incremental cost Section
F3 — Model-Implied Conviction
Score (MICS)
YES — fully
close
$0 11.1
F1 — Proprietary signal layer
(receptors)
YES —
receptors
only
$0 (free APIs) 11.2
F2 — Autonomous thesis
generation (low-fidelity)
YES — low
fidelity now
~$150/month 11.3
F4 — Learning loop (receptors) YES —
receptors
only
$0 11.4
F5 — Information-quality
confirmation windows
YES —
design
decision
now
$0 (design
choice)
11.5
F1 — Institutional data feeds
(full)
Phase 4 —
AUM
dependent
$50K–
$500K/year/feed
Future
F2 — High-fidelity autonomous
thesis generation
Phase 4 —
AUM
dependent
Institutional alt
data
Future
11.1 Model-Implied Conviction Score (MICS) — Build Time: 2-3 Days
Highest-value inch. Closes Frontier 3 almost completely. Zero new APIs. Zero ongoing cost.
MICS replaces the PM's free conviction level assignment with a scored output derived entirely from
SENTINEL gate data. The formula is pure Python arithmetic on data SENTINEL already produces. The
PM's role becomes a bounded confirmation — not a free assignment.
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 19
The formula
# Component weights — sum to 1.0
gate3_weight = 0.40 # Quantitative mispricing — core signal
gate6_weight = 0.30 # Source quality — information edge
gate4_weight = 0.15 # FEM impact — portfolio cleanliness
gate5_weight = 0.15 # Regime timing — entry quality
# Gate 3: normalize raw score (0-30) to 0-10
g3_score = (gate3_raw / 30) * 10
# Gate 6: source category -> score
source_scores = {'Cat A': 10, 'Cat B': 8, 'Cat C': 5, 'None': 4}
g6_score = source_scores[source_category]
# Gate 4: FEM impact -> score
fem_scores = {
'NORMAL->NORMAL': 10,
'NORMAL->WATCH': 7,
'WATCH->WATCH': 6,
'WATCH->ALERT (paired trim)':4
}
g4_score = fem_scores[fem_impact]
# Gate 5: regime at entry -> score
regime_scores = {
'RISK_ON': 10,
'WATCH': 9,
'NEUTRAL': 7,
'NEUTRAL (queued)': 5
}
g5_score = regime_scores[regime_at_entry]
# MICS raw (0.0 - 10.0 float)
MICS_raw = (g3_score * gate3_weight) +
(g6_score * gate6_weight) +
(g4_score * gate4_weight) +
(g5_score * gate5_weight)
# C-level (integer 1-10)
MICS = max(1, min(10, round(MICS_raw)))
PM override — bounded, not free
PM action Condition Process Audit
Accept MICS score Default Silence or one-tap
confirm
Auto-logged
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 20
Adjust ±1 level PM has specific
documented rationale
Written reason in Gate
6 form
Permanent
Adjust ±2 or more Extraordinary
circumstance only
GP co-sign required +
written rationale
Permanent +
GP flag
Category D attempt Not permitted System rejects. No
input field exists.
Rejection
logged
Retroactive scoring of current book
After MICS is built, run every current Architecture AB position through the formula using best available
proxy data for the original SENTINEL gate inputs. Where gate data is unavailable, use current Gate 3
scores and current source category estimates. Any position where MICS diverges from the current PM-
assigned C-level by more than 2 levels is flagged for GP review — not to force a change, but to surface
the divergence and require a documented explanation.
File src/engine/mics.py
Build time 2-3 days
Dependencies SENTINEL gate outputs only — no new APIs
Ongoing cost $0
Mile later CCM feeds quarterly calibration factor into MICS weights.
Scoring improves automatically from its own track record.
11.2 Feed-Agnostic Data Ingestion Pipeline — Build Time: 1 Week
Build the receptor now. The expensive feeds plug in later as configuration changes, not
code rebuilds.
Every data feed must be implemented as a plugin conforming to a standard FeedPlugin interface. The
pipeline does not care whether a feed comes from a free API or a $500K institutional subscription — it
only sees the interface. When alternative data becomes affordable, it is a new plugin, not a new
architecture.
FeedPlugin interface
class FeedPlugin(ABC):
@abstractmethod
def fetch(self) -> List[SignalRecord]: ...
# Every feed returns List[SignalRecord]
# regardless of source or cost tier
@dataclass class SignalRecord:
ticker: str # or 'MACRO' for macro signals
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 21
signal_type: str # e.g., 'EARNINGS_VELOCITY'
value: float # normalized 0-1 where applicable
raw_value: Any # original value before normalization
source: str # feed name e.g., 'SEC_EDGAR'
timestamp: str # ISO format
cost_tier: str # 'FREE' | 'LOW' | 'INSTITUTIONAL'
Free feeds to connect in Phase 1
Feed Signal type API Cost Mile later
SEC EDGAR full-
text
Earnings language
velocity, 13F position
changes, insider
filings
api.sec.gov — free $0 Replace with
institutional
13F analytics
FRED (Federal
Reserve)
Macro regime inputs:
yields, CPI, PCE,
credit spreads, PMI
api.stlouisfed.org
— free
$0 Already
institutional
quality — no
upgrade
needed
USPTO Patent
Bulk Data
Patent filing velocity
by company and
technology category
patentsview.org/api
— free
$0 Replace with
specialized
patent
analytics
Quiver Quantitative Congressional
trading disclosures,
dark pool flow,
institutional
ownership
quiverquant.com
— free tier
$0 Upgrade to
paid tier at
$50/month for
full flow
Adzuna Job
Postings API
Job posting velocity
as capex leading
indicator
api.adzuna.com —
free tier
$0 Replace with
Revelio Labs
or similar at
scale
MarineTraffic free
tier
Shipping activity as
supply chain proxy
marinetraffic.com
— free tier
$0 Replace with
Orbital Insight
satellite data
File src/data_feeds/free_signals.py + individual plugin files
Build time 1 week
Ongoing cost $0
Mile later Each free feed is replaced by an institutional equivalent by
swapping one plugin. The pipeline, ARAS, and all
downstream modules require zero changes.
11.3 Systematic Scan Engine — Build Time: 2 Weeks · ~$150/month
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 22
Low-fidelity autonomous thesis generation. PM shifts from finding ideas to evaluating
system candidates.
The Scan Engine runs every Monday pre-market against a defined universe of AI infrastructure
companies. It applies SENTINEL Gates 1 and 2 automatically using Claude API analysis of publicly
available earnings transcripts, SEC filings, and patent data. Any company passing both gates receives
a Gate 3 score from public valuation data. Results are delivered as a weekly intelligence briefing — not
as trade recommendations, but as candidates the PM has not yet examined.
Process
15. Pull the latest 10-K/10-Q/8-K filing and most recent earnings call transcript for each universe
company from SEC EDGAR (free).
16. Send filing and transcript to Claude API with a structured SENTINEL Gate 1 and Gate 2 prompt.
Request JSON output: {gate1_pass: bool, gate2_pass: bool, gate1_rationale: str,
gate2_rationale: str}.
17. For companies passing both gates, compute Gate 3 score from public valuation data (P/E vs
peers, institutional positioning from 13F, analyst consensus framing gap).
18. Generate weekly briefing: companies passing Gates 1-2 with Gate 3 scores, ranked by
mispricing score. Deliver to PM as Section 3 of Monday daily monitor.
19. PM reviews as intelligence — not as instructions. If a candidate matches pre-consensus
intelligence, PM initiates a full SENTINEL run.
Universe definition
Start with 50-75 companies across AI infrastructure: semiconductors (fabless and foundry-dependent),
networking, power/cooling infrastructure, data center REITs, cloud platforms, AI software with
infrastructure exposure. Add or remove tickers via a config file — no code changes required.
Cost estimation
Item Volume Unit cost Monthly cost
Claude API — Gate 1+2
analysis
75 companies × 4
weeks = 300 calls
~$0.40/call
average
~$120
Claude API — Gate 3 scoring ~40 pass rate × 4
weeks = 160 calls
~$0.20/call ~$32
SEC EDGAR filing pull API calls for
transcripts and
filings
$0 — free API $0
Total ~$150/month
File src/engine/systematic_scan.py
Runs Every Monday 5AM CT
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 23
Build time 2 weeks
Ongoing cost ~$150/month Claude API
Mile later Replace Claude API analysis with fine-tuned model on ARMS
proprietary thesis log. Replace free filing pulls with institutional
transcript service. Gate 3 scoring upgrades automatically as
free signal feeds are replaced with institutional alternatives.
11.4 Session Log Analytics (SLA) — Build Time: 1 Day
Three numbers monthly. The learning loop receptor. Zero cost. Feeds the Model
Optimization Engine in Phase 2.
SLA reads the session log ARMS already writes and outputs three metrics monthly. These metrics are
the foundation of the learning loop — when the CCM and Model Optimization Engine are built in Phase
2, they read from this same log. Build the structured log correctly now and the learning loop has
everything it needs when the time comes.
Metric Definition Why it matters
CDF accuracy rate % of positions that hit day-45 decay
and subsequently exited at a loss vs.
recovered. Measures whether the
45-day trigger is calibrated correctly.
If >70% of decayed positions
eventually exit at a loss, the trigger
is right. If <40%, the 45-day
window may be too short.
Regime transition lag Average days between first signal
elevation and formal regime call
across all transitions in the period.
Measures RPE pre-positioning
effectiveness.
As RPE matures, this lag should
shrink. Tracks whether pre-
positioning is working.
SENTINEL Gate 3
predictive accuracy
Spearman rank correlation between
Gate 3 scores at entry and
subsequent 90-day performance vs
QQQ. Measures whether the
mispricing score actually predicts
outperformance.
Feeds directly into CCM and MICS
weight optimization in Phase 2.
The most important long-run
metric in the system.
Session log structure — build this correctly from day one
Every system action must write to the session log with this minimum structure. If the log is unstructured,
SLA cannot read it and the learning loop has no data to consume.
@dataclass class SessionLogEntry:
timestamp: str # ISO format — millisecond precision
action_type: str # 'REGIME_CHANGE'|'TRADE'|'CDF_DECAY'|etc.
triggering_module: str # 'ARAS'|'PDS'|'MICS'|'CDF'|etc.
triggering_signal: str # human-readable rationale
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 24
ticker: Optional[str] # None for portfolio-level actions
mics_score: Optional[float] # at time of action
regime_at_action: str # canonical regime label
gate3_score: Optional[float] # for SENTINEL actions
source_category: Optional[str] # for SENTINEL actions
pm_override: bool # True if PM deviated from system rec
override_rationale: Optional[str]
outcome_90d: Optional[float] # filled in 90 days after entry
File src/reporting/audit_log.py +
src/engine/session_log_analytics.py
Build time 1 day (log structure + 3 metric calculations)
Ongoing cost $0
Mile later CCM reads outcome_90d field. Model Optimization Engine
reads all fields. Performance attribution by module reads
triggering_module. Everything flows from this log.
11.5 Information-Quality Confirmation Queue — Design Decision Now
This costs nothing extra to implement correctly at build time. It costs weeks to retrofit later.
Make this design decision today.
The current specification describes time-based veto windows (4 hours, 2 hours, 24 hours). This is
correct as a fallback. But the primary interface must be built around information quality, not elapsed
time. When the PM has nothing to add, they should be able to execute immediately — not wait out a 4-
hour clock. When they have Category A intelligence, they need as much time as they need. The design
decision is made now, at zero extra cost, because redesigning the interface in Phase 2 after LPs have
seen it is avoidable.
Three-option response interface — replace time-first with information-first
Response option Meaning System action Audit
Option 1: No new
information — execute
PM has reviewed the system
recommendation and has
nothing to add. Silence is trust in
the architecture.
Executes
immediately at
MICS-implied
sizing. No clock
delay.
Logged as 'PM
confirmed — no
new information'
Option 2: New
information present —
hold
PM has Cat A or B intelligence
that may change the
recommendation. Opens source
declaration form.
Pauses execution.
PM declares
source category
and specific
insight. System re-
runs Gate 3 with
updated source
score if Cat A/B is
Full source
declaration
logged
permanently
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 25
declared. MICS
updates. Execution
fires with updated
score.
Option 3: Veto with
rationale
PM disagrees with the system
recommendation and is blocking
execution.
No execution. PM
must write a
specific rationale.
Logged
permanently. If PM
vetoes more than 3
Tier 1
recommendations
in 30 days, GP
review triggered
automatically.
Permanent log +
frequency
monitoring
No response (time-
based fallback)
PM did not respond within the
defined window. Clock-based
default.
Executes at MICS-
implied sizing.
Identical to Option
1. Time window is
the fallback for PM
unavailability, not
the primary
interface.
Logged as 'PM
non-response —
system
executed'
Veto frequency monitoring — the override audit
If the PM vetoes more than 3 Tier 1 recommendations in any 30-day period, the system automatically
generates a veto frequency report for GP review. This is not punitive — it is informational. It surfaces
whether the PM and the system are systematically disagreeing, which is itself a signal. Either the model
needs recalibration or the PM's judgment is drifting from the architecture. Both are important to know.
File src/execution/confirmation_queue.py
Build time Part of Phase 1 brokerage integration sprint
Ongoing cost $0
Mile later When AUM supports it, the confirmation queue integrates with
a mobile app for push delivery and one-tap response. The
interface design does not change — only the delivery
mechanism.
11.6 Summary — Total Cost of Immediate-Build Frontiers
Build item Build time Ongoing cost Frontier
closed Mile it enables
ACHELION ARMS FSD — Master Build Document v1.1 | CONFIDENTIAL | Immediate-Build Frontiers Added
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction. 26
MICS formula (mics.py) 2-3 days $0 F3 — fully CCM weight
optimization in
Phase 2
Feed-agnostic pipeline + free
feeds
1 week $0 F1 — receptor Institutional
feeds plug in
as config
changes
Systematic Scan Engine 2 weeks ~$150/month F2 — low
fidelity
Fine-tuned
model
replaces
Claude API at
scale
Session Log Analytics 1 day $0 F4 — receptor CCM + Model
Opt Engine
read from this
log
Information-quality confirmation
queue
Part of
Phase 1
$0 F5 — fully Mobile app
delivery at
scale;
interface
unchanged
TOTAL ~4-5 weeks ~$150/month 3 fully closed
2 receptors
built
All 5 frontiers
accessible at
Phase 4
The total capital required to move all five frontiers from future aspiration to active receptor or full
implementation is approximately $150 per month. The total build time before any of this is in production
is four to five weeks for Josh working in parallel with Phase 1. There is no justification for waiting.
These are the inches. Build them.
"Silence is trust in the architecture."
Achelion Capital Management, LLC · Flow. Illumination. Discipline. Conviction.