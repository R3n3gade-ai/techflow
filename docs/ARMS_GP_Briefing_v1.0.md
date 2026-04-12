> **? STALE DOCUMENT � NOT AUTHORITATIVE**
> This document predates significant code changes (April 2026 remediation cycle).
> For current system truth, see: ARMS_NEXT_WAVE_COLD_TRUTH_AUDIT_2026-04-10.md
> and ARMS_REMEDIATION_MASTER_PLAN_2026-04-10.md

Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 1
ACHELION CAPITAL MANAGEMENT, LLC
Understanding ARMS
The Achelion Risk Management System
A Plain-Language Briefing for General Partners
March 2026 · Confidential — For General Partners Only
Most people love cars without knowing how combustion works. This
document explains the car. The engineering manuals exist — but this is not
one of them.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 2
A Note to the General Partners
ARMS — the Achelion Risk Management System — is the decision-making engine that runs
Achelion Capital. It determines how much risk we take, when we take it, when we pull back, and
how we protect capital when markets break. It does not replace judgment. It is the architecture
that ensures judgment is applied consistently, without the distortions of fear, greed, fatigue, or
overconfidence.
This document is written for you — the General Partners who represent Achelion to the world,
who sit across the table from LPs, and who need to understand what we have built well enough
to describe it with conviction. You do not need to know the code. You do need to know the logic.
Think of this as learning to fly a commercial aircraft as a passenger rather than a pilot. You will
never touch the controls. But you should know what the autopilot does, why it exists, and why
you can trust it more than a tired human at the controls at 35,000 feet.
ARMS is not a trading bot. It is a discipline engine. It ensures that the
decisions Achelion makes are always the decisions Achelion intended to make
— regardless of market conditions, time of day, or emotional climate.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 3
Glossary — Terms You Will Encounter
Every term below appears in this document. Read this section once. Return to it as needed.
ARMS
Achelion Risk Management System. The complete decision and execution
architecture that governs how Achelion manages capital. Not a single tool
— a system of seven interconnected modules.
Architecture AB The canonical portfolio structure: 58% equities, 20% digital assets, 14%
defensive sleeve, 8% cash. 'AB' stands for Achelion Base.
Regime
The market environment we are currently operating in. ARMS identifies
five regimes — from most aggressive to most defensive. The regime
determines how much risk we are allowed to carry.
Regime ceiling
The maximum equity exposure allowed in each regime. In the most
defensive regime, we can only hold 15% in equities. In the most
aggressive, we can hold 100%. The ceiling is automatic and cannot be
overridden without documented GP approval.
Conviction
score
A number from 1 to 10 that represents our confidence in a position.
Higher conviction = larger position size. The formula squares the score,
so a C10 position carries 4 times the weight of a C5. This is mathematical
concentration discipline — bet big on what you know, small on what you
are learning.
MICS
Model-Implied Conviction Score. The formula ARMS uses to derive the
conviction score from objective data — rather than relying on the PM's
subjective opinion. The PM can adjust it by one level with a written
reason. That is the full extent of PM involvement in sizing.
SENTINEL
The six-gate protocol that every new investment must pass before
entering the portfolio. Think of it as a six-question interview that every
position must answer correctly before we invest a dollar.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 4
Defensive sleeve
14% of the portfolio permanently allocated to instruments that hold value
or gain value when markets fall: short-term Treasury bills (SGOV), gold
(SGOL), managed futures (DBMF), and structured credit (STRC). The
sleeve is not a hedge — it is structural protection that is always present.
PTRH
Permanent Tail Risk Hedge. We always hold put options on the Nasdaq-
100 ETF (QQQ). These options pay off if technology stocks fall sharply.
Always on. Never removed. Think of it as permanent insurance.
SLOF
Synthetic Leverage Overlay Facility. A tool that allows us to amplify
returns on our highest-conviction positions without borrowing money.
Only used in the two most aggressive market regimes. Automatically
deactivated when markets deteriorate.
PERM
Profit-locking mechanism. When a position has risen more than 30%
from our entry price, ARMS evaluates selling covered call options against
it. This collects cash premium from other investors and provides a buffer
if the position reverses. Protects gains without selling the position.
CDF
Conviction Decay Function. If a position underperforms the Nasdaq-100
by more than 10 percentage points for 45 consecutive days, its weight in
the portfolio automatically begins to shrink — without requiring the PM
to make a sell decision. At day 135 without improvement, a mandatory
review is triggered.
ARAS
Achelion Risk Assessment System. The module that continuously scores
the current market environment and outputs the current regime and
ceiling. The brain of ARMS.
PDS
Portfolio Drawdown Sentinel. An independent safety mechanism that
watches the portfolio's total value against its all-time high. If we fall 12%
from our peak, exposure automatically reduces to 60%. If we fall 18%, it
reduces to 30%. This fires regardless of what any other module says.
FEM
Factor Exposure Monitor. Detects hidden concentration risk. Our
portfolio may look diversified across 12 companies — but if 80% of those
companies share the same dependence on AI chip manufacturing in
Taiwan, we are effectively running a single concentrated bet. FEM
surfaces this.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 5
Session log
The immutable record of every decision ARMS makes. Every trade, every
regime change, every flag, every override — logged with a timestamp, the
reason, and the module that triggered it. Cannot be edited. LP-auditable.
Tier 0 / Tier 1 /
Tier 2
The three levels of decision authority. Tier 0: the system acts immediately
with no human input. Tier 1: the system acts unless the PM vetoes within
a defined window. Tier 2: the system recommends, a human must
confirm. No decision can be escalated from Tier 0 to Tier 1 without GP
documentation.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 6
What ARMS Does — In One Paragraph
ARMS watches markets continuously, identifies the current environment, sets
the maximum risk we are allowed to take, sizes every position according to a
formula rather than opinion, protects capital automatically when things
deteriorate, harvests gains from winning positions, and generates a complete
daily report — all without human involvement. The PM's job is to identify
which companies belong in the portfolio. Everything after that decision is
ARMS.
The analogy we use internally: ARMS is the flight control computer on an F-22 fighter jet. The
pilot — our PM — declares the mission and identifies the target. The computer translates that
intent into precise control surface movements the human could never execute fast enough or
accurately enough. The pilot does not manage individual aileron deflections. The pilot flies the
mission. The computer flies the jet.
What this means for our LPs: they are not betting on our PM's ability to make good decisions
every day under pressure. They are betting on an architecture that was specifically designed to
perform when markets are most difficult — because that is precisely when human judgment is
most compromised.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 7
The Five Regimes — Reading the Room
ARMS identifies the current market environment every five minutes and classifies it into one of
five regimes. The regime is not a forecast — it is a present-tense assessment of current
conditions. Think of it as ARMS continuously asking: 'Given what the market is doing right
now, how much should we have at risk?' The answer changes the portfolio ceiling automatically.
The regime is determined by a composite score derived from multiple signals: growth
momentum, inflation trends, oil prices, interest rate trajectory, credit conditions, volatility
levels, and geopolitical event risk. No single signal controls the outcome — it is a weighted
combination, like a pilot reading multiple instruments simultaneously.
Regime Score
range
Equity
ceiling SLOF status What it means
RISK_ON 0.00 –
0.30
100% Active — full
deployment
Everything is working. Growth is
strong, markets are calm, risk is
rewarded. We are fully invested
and using our conviction
amplifier.
WATCH 0.31 –
0.50
100% Active —
monitoring
Conditions are mostly positive
but something is worth watching.
We remain fully invested but the
system is on alert. Defense is
beginning to build.
NEUTRAL 0.51 –
0.65
75% Reducing The environment is mixed. We
pull back to 75% equity exposure.
The conviction amplifier begins
to reduce. We are cautious but
not defensive.
DEFENSIVE 0.66 –
0.80
40% Removed Conditions are deteriorating. We
hold a maximum of 40% in
equities. The conviction amplifier
is off. The defensive sleeve and
tail hedge are working. We are
protecting capital.
CRASH 0.81 –
1.00
15% Removed Markets are in freefall. We hold a
maximum of 15% in equities.
Everything else is in capital
preservation mode. No new
positions. No amplification.
Survival first.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 8
One important nuance: the regime is not a forecast. ARMS does not predict where the market is
going. It identifies where it is right now and manages risk accordingly. This is a crucial
distinction. Many funds try to predict the future. ARMS responds to the present — faster and
more accurately than any human can.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 9
The Seven Pillars — How ARMS Is Built
ARMS is not a single system. It is seven interconnected modules — we call them pillars — each
responsible for a specific function. Together they form a complete architecture. Remove any one
and the system has a gap. All seven must operate simultaneously for ARMS to function as
designed.
Think of the seven pillars as the seven systems on a commercial aircraft: engines, navigation,
hydraulics, pressurization, electrical, communications, and landing gear. Each does something
distinct. Each depends on the others. The plane does not fly on six.
1
ARAS · Achelion Risk Assessment System · The brain.
ARAS continuously reads the market — growth data, inflation signals, oil prices, interest
rates, credit conditions, volatility — and produces the current regime label and ceiling.
Every other module takes its instructions from ARAS. It runs every five minutes, twenty-
four hours a day. If markets move at 3am, ARAS knows.
Analogy: The air traffic controller. Constantly scanning the environment, telling the pilot
what altitude to fly at given current conditions.
2
Macro Compass · Regime Detection Engine · The navigator.
The Macro Compass is the sub-system inside ARAS that converts raw market data into the
regime score. It weighs multiple signals and produces a single number between 0 and 1.
Below 0.50 is the optimistic half. Above 0.65 is the defensive zone. The score tells us not
just which regime we are in — but where we sit within that regime, how close we are to a
boundary, and which direction we are moving.
Analogy: The instrument panel. Not just showing speed — showing rate of acceleration,
fuel consumption, and distance to the next waypoint simultaneously.
3
Master Engine · Portfolio Construction · The builder.
The Master Engine takes the regime ceiling from ARAS and the conviction scores from
MICS, and calculates the precise target weight for every position. It enforces the ceiling
automatically. It applies the conviction-squared weighting formula. It incorporates any
conviction decay factors from underperforming positions. The PM does not set position
sizes — the Master Engine calculates them.
Analogy: The autopilot's flight management computer. Given the destination, altitude
constraints, and fuel load — it calculates the precise control inputs required. The pilot does
not manually calculate thrust settings.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 10
4
KEVLAR · Position Limits · The guardrails.
KEVLAR enforces hard maximum position sizes regardless of what any other module
says. No single position can grow beyond its KEVLAR limit — not because of conviction,
not because of performance, not because the PM believes in it. KEVLAR exists to prevent
the catastrophic scenario where one position becomes so large that it threatens the entire
portfolio. It is the structural steel in the building.
Analogy: The speed limiter on a car. No matter how hard you press the accelerator, the
car will not exceed 155mph. The driver's intention is irrelevant. The limit is structural.
5
PERM · Profit Protection · The harvester.
When a position has risen more than 30% from our entry price, PERM evaluates whether
to sell covered call options against it. If it does, we collect cash from other investors who
want to bet the position will keep rising sharply. That cash is ours regardless of what
happens next. If the position keeps rising, we participate — but less. If it falls, the cash we
collected cushions the impact. PERM also manages the Conviction Decay Function, which
automatically reduces the size of positions that are underperforming.
Analogy: The farmer who sells a portion of next season's crop at today's prices once they
have a good harvest. They lock in some of the gain. They still benefit from further growth.
They protect against a bad season.
6
SLOF · Conviction Amplifier · The accelerator.
SLOF is the only module that adds risk rather than removing it. When we are in RISK_ON
or WATCH regime and we have a position at our highest conviction level (C10), SLOF
allows us to amplify the return on that position using a synthetic structure that mimics
owning double the shares. It is only deployed on our absolute highest-conviction
positions, only in the most favorable market conditions, and is automatically removed the
moment conditions deteriorate. It is a precision tool, not a lever we pull freely.
Analogy: The afterburner on a fighter jet. Extraordinary additional power available only
in specific conditions. The pilot does not fly with it constantly — it burns fuel too fast. It is
reserved for the moments when maximum performance is required and the conditions
support it.
7
ARES · Re-entry System · The re-builder.
When ARMS has deleveraged — reduced exposure because conditions deteriorated —
ARES manages the return to full deployment. It checks four conditions before allowing
any increase in exposure: the regime must have improved, volatility must be declining, the
specific trigger that caused the deleverage must have resolved, and the composite risk
score must have fallen sufficiently. Re-entry happens in three tranches over several days.
We never go back to full exposure in one movement. We test the ground before putting
full weight on it.
Analogy: The aircraft landing system that requires multiple conditions to be met before
touchdown: correct speed, correct altitude, correct approach angle, landing gear
confirmed down. Not one condition — all four. In sequence.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 11
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 12
The SENTINEL Protocol — How We Choose
What We Own
Every position in the Achelion portfolio must pass six questions before we invest a dollar. We
call this the SENTINEL protocol. It is the most important discipline in the system — because
the best risk management begins with owning the right things in the first place.
Most funds ask one question: will this go up? SENTINEL asks six. Each question must be
answered correctly. A single failure means the position does not enter the portfolio — regardless
of how compelling the story sounds, how many analysts recommend it, or how much conviction
the PM has.
A compelling story is exactly what SENTINEL is designed to resist. History is
full of investments that had a compelling story and destroyed capital. The
gates exist to separate conviction from narrative.
Gate 1 · Is this a civilizational shift — not a product cycle?
Does this company sit inside a change that will restructure the global economy regardless of
whether any individual product succeeds? We only invest in companies that are non-optional
components of the way the future will work. We do not invest in trends. We invest in
infrastructure.
Example: We would not have invested in any individual social media app. We would have
invested in the companies that built the cloud infrastructure every app ran on.
Gate 2 · Can the world route around this company?
If this company ceased to exist tomorrow, could the market replace what it does within 18
months? If yes — the company is replaceable and its pricing power is limited. We need
companies that cannot be routed around. Structural necessity, not temporary advantage.
Example: NVIDIA cannot currently be routed around for certain AI computing tasks. A
company that makes generic memory chips can be replaced by any of ten competitors. One
passes Gate 2. The other does not.
Gate 3 · Is the market pricing this incorrectly?
This gate uses a quantitative formula — not an opinion. It scores the company's valuation
relative to similar companies, the gap between where large institutional investors are positioned
and where the thesis says they should be, and whether the investment narrative the market is
using to value this company is the wrong one. The score must exceed a defined threshold. A
compelling argument does not substitute for the number.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 13
Example: Alphabet (Google) was valued as an advertising company while becoming one of
three sovereign-scale AI computing platforms. The market was using the wrong identity to price
it. That gap is what Gate 3 detects.
Gate 4 · Does this position make the portfolio safer or more dangerous?
The portfolio already holds 12 positions. Adding a 13th changes the concentration of risk across
the whole book. Gate 4 runs a factor analysis — does this new position increase our dependence
on a single theme (like AI chip manufacturing in Taiwan) beyond safe limits? If it does, we
cannot add the position without simultaneously reducing another.
Example: You would not add a 13th passenger to a 12-passenger boat without first checking
whether the hull can handle the additional weight — and whether adding that passenger changes
the balance in a way that makes the boat less stable.
Gate 5 · Is this the right time?
This gate is fully automated. The current market regime determines whether we are allowed to
initiate new positions. In DEFENSIVE regime, new positions are blocked and queued until
conditions improve. In CRASH regime, nothing new enters the portfolio. The system will not
override this gate regardless of how attractive the opportunity looks. Timing discipline is not
optional.
Example: You do not launch a rocket into a thunderstorm, regardless of how perfect the payload
is or how long you have been preparing. You wait for the right launch window.
Gate 6 · What do you know and how do you know it?
This is the only human gate in the protocol. If the PM is bringing a new idea to the table, they
must declare the source of their insight from a defined list: a direct conversation with someone
inside the company or supply chain (highest value), recognition of a pattern from prior market
cycles (high value), or synthesis of publicly available information (lower value — requires a
higher score on Gate 3 to compensate). Gut feelings and strong opinions are not a valid source
category. They do not exist in the system.
Example: A surgeon who says 'I have a feeling about this diagnosis' is held to a different
standard than one who says 'I spoke with the patient's referring physician and reviewed the prior
imaging.' Both may be right. One is defensible. One is not.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 14
The Daily Flow — What Happens Every Day
ARMS does not sleep. Markets move twenty-four hours a day. Geopolitical events happen at
3am. Oil prices shift before New York opens. ARMS processes all of it continuously. Below is
the flow of a typical day.
All night Data
ingestion
ARMS continuously monitors market signals, macro data,
oil prices, volatility indicators, and geopolitical feeds. The
regime score updates every five minutes.
5:15 AM CT Portfolio
snapshot
ARMS takes a precise reading of every position — current
price, weight, conviction score, decay status, unrealized
gain/loss. This is the baseline for the day.
5:20 AM CT Module
sweep
All seven pillars run simultaneously: factor exposure check,
drawdown sentinel check, tail hedge status, conviction decay
update, stress scenario computation.
5:30 AM CT
Daily
monitor
compiled
ARMS assembles the complete daily report — regime
assessment, position status, all flags, all alerts, decision
queue — and generates it as a digital document.
6:00 AM CT Monitor
delivered
The PM and all General Partners receive the daily monitor.
No human assembled it. No human edited it. It reflects the
state of the portfolio exactly as ARMS sees it.
Market open
(9:30)
Live
execution
mode
Any Tier 0 actions — regime ceiling enforcement, position
size adjustments, tail hedge rolls — execute automatically as
market conditions warrant. No human required.
During
market
hours
Continuous
monitoring
ARMS watches every position, every macro signal, and every
module trigger in real time. If something requires action, it
acts (Tier 0) or notifies the PM (Tier 1) immediately.
Weekly
(Monday)
Scan Engine
runs
ARMS automatically screens the AI infrastructure
investment universe — 50 to 75 companies — against the
first two SENTINEL gates. Candidates that pass are surfaced
to the PM as an intelligence briefing.
Monthly
(1st)
Learning
loop runs
ARMS reviews its own decisions from the prior month. Were
the positions it flagged for concern actually problems? Did
its conviction scores predict outcomes? The system scores
itself and adjusts accordingly.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 15
What Humans Do — And What They Do Not
One of the questions GPs are most likely to hear from LPs is: 'If the system does all of this, what
does the PM actually do?' This is the right question. The answer is important.
The PM does the one thing no algorithm can replicate: he sees the future
before it is in the data. Everything else is the system.
Achelion's PM brings 28 years of market pattern recognition — the ability to identify a
civilizational shift before it reaches mainstream consensus and before the data confirms it. The
Tesla thesis. The AI infrastructure thesis. These were not data conclusions. They were pattern
recognitions. A human who has seen multiple market cycles can identify when a company is
being valued for what it used to be rather than what it is becoming. That is not a skill algorithms
currently possess.
Once the PM identifies a candidate and brings it through the SENTINEL protocol, the system
takes over. Here is the precise boundary:
The PM does this The PM does not do this
Identifies companies that represent
civilizational shifts before the market prices
them correctly
Brings pattern recognition from lived
experience across multiple market cycles
Seeds new SENTINEL analyses with a thesis —
why this company, why now
Declares the source of the insight (direct
knowledge, pattern recognition, or public
synthesis)
Reviews and confirms or vetoes Tier 1 system
recommendations within defined time
windows
Builds and maintains relationships with LPs
and the investment community
Holds the strategic vision for Achelion Capital
Set position sizes — the MICS formula does
this
Execute trades — the execution layer does this
automatically
Decide when to deleverage — ARAS and PDS
do this automatically
Override the regime ceiling — this requires
documented GP co-sign
Decide when to re-enter — ARES manages re-
entry in tranches
Manage the tail hedge — PTRH rolls and
resizes this automatically
Make gut-feel decisions under pressure — the
system exists precisely to prevent this
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 16
What Makes Achelion Different — The Honest
Answer
Every hedge fund tells LPs they have a disciplined process. What they mean is that their PM has
good intentions and tries to be disciplined. ARMS makes the discipline structural. The
difference is the difference between a driver who tries not to speed and a car with a speed
limiter. One depends on willpower under pressure. The other does not.
Here is what Achelion can say that almost no other fund of any size can say truthfully:
Every sizing decision is derived from a formula, not an opinion.
The MICS formula converts SENTINEL gate data into a model-implied conviction score. The
PM can adjust it by one level with a written reason. That is the full extent of human involvement
in position sizing. No other emerging fund operates this way.
The regime ceiling cannot be overridden by the PM alone.
If ARMS says we are in DEFENSIVE regime and our equity ceiling is 40%, the PM cannot
change that unilaterally. A GP co-sign and documented justification are required. This is not a
policy. It is structural — the system enforces it.
Every decision is logged with the reason it was made.
The session log records every trade, every regime change, every flag, every override. It cannot be
edited. An LP, auditor, or regulator can verify that the system ran exactly as described in any
document we have provided — in any session, on any date.
The defensive architecture was validated through the worst tech year since
2000.
The 2022 backtest shows ARMS at −16.1% in a year when the Nasdaq-100 fell 32.6%. The
defensive sleeve, the tail hedge, and the regime-driven deleverage all performed as designed
when it mattered most. We did not project this. We demonstrated it.
The PM's job is to see the future — not to manage the process.
Most fund managers spend the majority of their time on portfolio mechanics — what to buy,
when to buy, how much, when to sell. ARMS handles all of that. Our PM spends time on the one
thing that produces alpha: identifying what the world will look like before the market prices it
in.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 17
Questions GPs Will Hear — Suggested
Responses
The following questions are the ones LPs ask most often about systematic and AI-assisted
portfolio management. These are not scripted answers — they are frameworks for honest
responses that build trust.
"What happens when the system is wrong?"
ARMS is not designed to be always right. It is designed to be wrong in ways that are survivable.
When the regime model misreads the environment — and it will, occasionally — the structural
safeguards still apply. The tail hedge is always on. The drawdown sentinel fires at −12%. The
defensive sleeve is always present. The system fails gracefully. Most funds fail catastrophically,
because there is no architecture — just a PM who was wrong.
"What if the AI makes a bad decision?"
ARMS does not make decisions. It enforces rules. There is no AI deciding which stock to buy.
There is a formula that calculates a conviction score. There is a protocol that gates every new
position through six questions. There is a scheduler that enforces ceilings automatically. The
intelligence of the system is in its design — not in real-time discretion. When we say AI, we
mean the analytical layer that helps assess investment candidates and generate reports — not
an autonomous agent trading our capital.
"What does the PM actually do?"
The PM does the one thing no algorithm can currently replicate: he sees the future before it is in
the data. His job is to identify companies that the market is pricing incorrectly because it is
using the wrong frame of reference. Once he identifies a candidate, the system evaluates it
through six gates. If it passes, the system manages it from entry through exit. The PM's job is
vision. The system's job is execution.
"How is this different from a quant fund?"
Quant funds find patterns in historical data and bet that those patterns will repeat. We do not
trade patterns. We invest in the companies that are building the next era of global
infrastructure — and we use the system to ensure we stay invested in them correctly, protect
capital when markets break, and do not make emotional decisions under pressure. The thesis is
human. The discipline is systemic.
"What is your track record?"
Achelion has not yet begun live fund operations. What we have is a full-cycle backtest — a
three-year simulation (2020-2022) of ARMS applied to actual historical market conditions,
covering the fastest bear market in history, the most speculative bull run of our era, and the
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 18
worst year for technology stocks since 2000. The result: +47.4% over three years versus the
S&P 500's +24.8%. The 2022 preservation result was −16.1% versus −18.1% for the S&P 500 —
in a year when we carried a 20% allocation to digital assets that fell 65%. The system worked
when it was hardest. We show you the full cycle — not our best year.
"Can I see the system running?"
Yes. Every morning, the system generates a daily monitor that shows the current regime, every
position with its status and flags, all active alerts, and the decision queue. It is assembled
automatically, without human involvement, and reflects the exact state of the portfolio. We are
happy to share a sample monitor during due diligence. You will see the architecture working —
not a pitch deck claiming it works.
Understanding ARMS — General Partner Briefing · Achelion Capital Management, LLC · CONFIDENTIAL
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution 19
In Summary
ARMS is not a feature. It is the fund. Every conviction-weighted position, every regime-driven
ceiling, every automatic deleverage, every gain-harvesting covered call, every re-entry tranche
— all of it is the architecture expressing its design.
The Wall Street model is built on trust in individuals. Achelion is built on trust in architecture.
We believe the LP who understands this distinction — who recognizes that the system cannot
panic, cannot fall in love with a position, cannot rationalize holding something that should be
sold, cannot be tired at 2am when a geopolitical event moves markets — will find that
distinction deeply reassuring.
We are not asking LPs to trust our PM's judgment in the moment. We are asking them to
evaluate the quality of the architecture we built before the moment arrived.
Far more money has been lost on Wall Street by investors who believed in
salesmen than by investors who believed in systems. We built a system. Come
and inspect it.
"Silence is trust in the architecture."
Achelion Capital Management, LLC
Flow. Illumination. Discipline. Conviction.
