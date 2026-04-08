# Understanding ARMS — General Partner Briefing
Achelion Capital Management, LLC · For General Partners Only · Not for Distribution

*Most people love cars without knowing how combustion works. This document explains the car. The engineering manuals exist — but this is not one of them.*

## A Note to the General Partners
ARMS — the Achelion Risk Management System — is the decision-making engine that runs Achelion Capital. It determines how much risk we take, when we take it, when we pull back, and how we protect capital when markets break. It does not replace judgment. It is the architecture that ensures judgment is applied consistently, without the distortions of fear, greed, fatigue, or overconfidence.

This document is written for you — the General Partners who represent Achelion to the world, who sit across the table from LPs, and who need to understand what we have built well enough to describe it with conviction. You do not need to know the code. You do need to know the logic. Think of this as learning to fly a commercial aircraft as a passenger rather than a pilot. You will never touch the controls. But you should know what the autopilot does, why it exists, and why you can trust it more than a tired human at the controls at 35,000 feet.

> **ARMS is not a trading bot. It is a discipline engine.** It ensures that the decisions Achelion makes are always the decisions Achelion intended to make — regardless of market conditions, time of day, or emotional climate.

## Glossary — Terms You Will Encounter
Every term below appears in this document. Read this section once. Return to it as needed.

* **ARMS**: Achelion Risk Management System. The complete decision and execution architecture that governs how Achelion manages capital. Not a single tool — a system of seven interconnected modules.
* **Architecture AB**: The canonical portfolio structure: 58% equities, 20% digital assets, 14% defensive sleeve, 8% cash. 'AB' stands for Achelion Base.
* **Regime**: The market environment we are currently operating in. ARMS identifies five regimes — from most aggressive to most defensive. The regime determines how much risk we are allowed to carry.
* **Regime ceiling**: The maximum equity exposure allowed in each regime. In the most defensive regime, we can only hold 15% in equities. In the most aggressive, we can hold 100%. The ceiling is automatic and cannot be overridden without documented GP approval.
* **Conviction score**: A number from 1 to 10 that represents our confidence in a position. Higher conviction = larger position size. The formula squares the score, so a C10 position carries 4 times the weight of a C5. This is mathematical concentration discipline — bet big on what you know, small on what you are learning.
* **MICS**: Model-Implied Conviction Score. The formula ARMS uses to derive the conviction score from objective data — rather than relying on the PM's subjective opinion. The PM can adjust it by one level with a written reason. That is the full extent of PM involvement in sizing.
* **SENTINEL**: The six-gate protocol that every new investment must pass before entering the portfolio. Think of it as a six-question interview that every position must answer correctly before we invest a dollar.
* **Defensive sleeve**: 14% of the portfolio permanently allocated to instruments that hold value or gain value when markets fall: short-term Treasury bills (SGOV), gold (SGOL), managed futures (DBMF), and structured credit (STRC). The sleeve is not a hedge — it is structural protection that is always present.
* **PTRH**: Permanent Tail Risk Hedge. We always hold put options on the Nasdaq-100 ETF (QQQ). These options pay off if technology stocks fall sharply. Always on. Never removed. Think of it as permanent insurance.
* **SLOF**: Synthetic Leverage Overlay Facility. A tool that allows us to amplify returns on our highest-conviction positions without borrowing money. Only used in the two most aggressive market regimes. Automatically deactivated when markets deteriorate.
* **PERM**: Profit-locking mechanism. When a position has risen more than 30% from our entry price, ARMS evaluates selling covered call options against it. This collects cash premium from other investors and provides a buffer if the position reverses. Protects gains without selling the position.
* **CDF**: Conviction Decay Function. If a position underperforms the Nasdaq-100 by more than 10 percentage points for 45 consecutive days, its weight in the portfolio automatically begins to shrink — without requiring the PM to make a sell decision. At day 135 without improvement, a mandatory review is triggered.
* **ARAS**: Achelion Risk Assessment System. The module that continuously scores the current market environment and outputs the current regime and ceiling. The brain of ARMS.
* **PDS**: Portfolio Drawdown Sentinel. An independent safety mechanism that watches the portfolio's total value against its all-time high. If we fall 12% from our peak, exposure automatically reduces to 60%. If we fall 18%, it reduces to 30%. This fires regardless of what any other module says.
* **FEM**: Factor Exposure Monitor. Detects hidden concentration risk. Our portfolio may look diversified across 12 companies — but if 80% of those companies share the same dependence on AI chip manufacturing in Taiwan, we are effectively running a single concentrated bet. FEM surfaces this.
* **Session log**: The immutable record of every decision ARMS makes. Every trade, every regime change, every flag, every override — logged with a timestamp, the reason, and the module that triggered it. Cannot be edited. LP-auditable.
* **Tier 0 / Tier 1 / Tier 2**: The three levels of decision authority. Tier 0: the system acts immediately with no human input. Tier 1: the system acts unless the PM vetoes within a defined window. Tier 2: the system recommends, a human must confirm. No decision can be escalated from Tier 0 to Tier 1 without GP documentation.
* **LAEP**: Liquidity-Adjusted Execution Protocol. The module that governs how orders are executed based on current market volatility. In NORMAL mode (VIX below 25): 30-minute VWAP windows, 8bps slippage budget — efficient, clean fills. In ELEVATED mode (VIX 25–45): 60-minute VWAP windows, 20bps slippage budget — wider execution window to avoid moving the market. In CRISIS mode (VIX above 45): orders break into smaller tranches across multiple sessions. The mode is determined automatically — the PM does not set it. When the deployment queue fires, LAEP ensures positions are built at appropriate market impact levels for current conditions.

## What ARMS Does — In One Paragraph
ARMS watches markets continuously, identifies the current environment, sets the maximum risk we are allowed to take, sizes every position according to a formula rather than opinion, protects capital automatically when things deteriorate, harvests gains from winning positions, and generates a complete daily report — all without human involvement. The PM's job is to identify which companies belong in the portfolio. Everything after that decision is ARMS.

The analogy we use internally: ARMS is the flight control computer on an F-22 fighter jet. The pilot — our PM — declares the mission and identifies the target. The computer translates that intent into precise control surface movements the human could never execute fast enough or accurately enough. The pilot does not manage individual aileron deflections. The pilot flies the mission. The computer flies the jet.

What this means for our LPs: they are not betting on our PM's ability to make good decisions every day under pressure. They are betting on an architecture that was specifically designed to perform when markets are most difficult — because that is precisely when human judgment is most compromised.

## The Five Regimes — Reading the Room
ARMS identifies the current market environment every five minutes and classifies it into one of five regimes. The regime is not a forecast — it is a present-tense assessment of current conditions. Think of it as ARMS continuously asking: 'Given what the market is doing right now, how much should we have at risk?' The answer changes the portfolio ceiling automatically.

The regime is determined by a composite score derived from multiple signals: growth momentum, inflation trends, oil prices, interest rate trajectory, credit conditions, volatility levels, and geopolitical event risk. No single signal controls the outcome — it is a weighted combination, like a pilot reading multiple instruments simultaneously.

| Regime | Score Range | Equity Ceiling | SLOF Status | What it means |
|---|---|---|---|---|
| **RISK_ON** | 0.00 – 0.30 | 100% | Active — full deployment | Everything is working. Growth is strong, markets are calm, risk is rewarded. We are fully invested and using our conviction amplifier. |
| **WATCH** | 0.31 – 0.50 | 100% | Active — monitoring | Conditions are mostly positive but something is worth watching. We remain fully invested but the system is on alert. Defense is beginning to build. |
| **NEUTRAL** | 0.51 – 0.65 | 75% | Reducing | The environment is mixed. We pull back to 75% equity exposure. The conviction amplifier begins to reduce. We are cautious but not defensive. |
| **DEFENSIVE** | 0.66 – 0.80 | 40% | Removed | Conditions are deteriorating. We hold a maximum of 40% in equities. The conviction amplifier is off. The defensive sleeve and tail hedge are working. We are protecting capital. |
| **CRASH** | 0.81 – 1.00 | 15% | Removed | Markets are in freefall. We hold a maximum of 15% in equities. Everything else is in capital preservation mode. No new positions. No amplification. Survival first. |

One important nuance: the regime is not a forecast. ARMS does not predict where the market is going. It identifies where it is right now and manages risk accordingly. This is a crucial distinction. Many funds try to predict the future. ARMS responds to the present — faster and more accurately than any human can.

## The Seven Pillars — How ARMS Is Built
ARMS is not a single system. It is seven interconnected modules — we call them pillars — each responsible for a specific function. Together they form a complete architecture. Remove any one and the system has a gap. All seven must operate simultaneously for ARMS to function as designed.

Think of the seven pillars as the seven systems on a commercial aircraft: engines, navigation, hydraulics, pressurization, electrical, communications, and landing gear. Each does something distinct. Each depends on the others. The plane does not fly on six.

**1. ARAS · Achelion Risk Assessment System · The brain.**
ARAS continuously reads the market — growth data, inflation signals, oil prices, interest rates, credit conditions, volatility — and produces the current regime label and ceiling. Every other module takes its instructions from ARAS. It runs every five minutes, twenty-four hours a day. If markets move at 3am, ARAS knows. (Analogy: The air traffic controller.)

**2. Macro Compass · Regime Detection Engine · The navigator.**
The Macro Compass is the sub-system inside ARAS that converts raw market data into the regime score. It weighs multiple signals and produces a single number between 0 and 1. Below 0.50 is the optimistic half. Above 0.65 is the defensive zone. The score tells us not just which regime we are in — but where we sit within that regime, how close we are to a boundary, and which direction we are moving. (Analogy: The instrument panel.)

**3. Master Engine · Portfolio Construction · The builder.**
The Master Engine takes the regime ceiling from ARAS and the conviction scores from MICS, and calculates the precise target weight for every position. It enforces the ceiling automatically. It applies the conviction-squared weighting formula. It incorporates any conviction decay factors from underperforming positions. The PM does not set position sizes — the Master Engine calculates them. (Analogy: The autopilot's flight management computer.)

**4. KEVLAR · Position Limits · The guardrails.**
KEVLAR enforces hard maximum position sizes regardless of what any other module says. No single position can grow beyond its KEVLAR limit — not because of conviction, not because of performance, not because the PM believes in it. KEVLAR exists to prevent the catastrophic scenario where one position becomes so large that it threatens the entire portfolio. (Analogy: The speed limiter on a car.)

**5. PERM · Profit Protection · The harvester.**
When a position has risen more than 30% from our entry price, PERM evaluates whether to sell covered call options against it. If it does, we collect cash from other investors who want to bet the position will keep rising sharply. That cash is ours regardless of what happens next. If the position keeps rising, we participate — but less. If it falls, the cash we collected cushions the impact. (Analogy: The farmer who sells a portion of next season's crop at today's prices once they have a good harvest.)

**6. SLOF · Conviction Amplifier · The accelerator.**
SLOF is the only module that adds risk rather than removing it. When we are in RISK_ON or WATCH regime and we have a position at our highest conviction level (C10), SLOF allows us to amplify the return on that position using a synthetic structure that mimics owning double the shares. It is only deployed on our absolute highest-conviction positions, only in the most favorable market conditions, and is automatically removed the moment conditions deteriorate. (Analogy: The afterburner on a fighter jet.)

**7. ARES · Re-entry System · The re-builder.**
When ARMS has deleveraged — reduced exposure because conditions deteriorated — ARES manages the return to full deployment. It checks four conditions before allowing any increase in exposure: the regime must have improved, volatility must be declining, the specific trigger that caused the deleverage must have resolved, and the composite risk score must have fallen sufficiently. Re-entry happens in three tranches over several days. We never go back to full exposure in one movement. (Analogy: The aircraft landing system that requires multiple conditions to be met before touchdown.)

## The SENTINEL Protocol — How We Choose What We Own
Every position in the Achelion portfolio must pass six questions before we invest a dollar. We call this the SENTINEL protocol. It is the most important discipline in the system — because the best risk management begins with owning the right things in the first place.

> A compelling story is exactly what SENTINEL is designed to resist. History is full of investments that had a compelling story and destroyed capital. The gates exist to separate conviction from narrative.

**Gate 1 · Is this a civilizational shift — not a product cycle?**
Does this company sit inside a change that will restructure the global economy regardless of whether any individual product succeeds? We do not invest in trends. We invest in infrastructure. (Example: The companies that built the cloud infrastructure every app ran on, not the apps.)

**Gate 2 · Can the world route around this company?**
If this company ceased to exist tomorrow, could the market replace what it does within 18 months? If yes — the company is replaceable and its pricing power is limited. We need companies that cannot be routed around. (Example: NVIDIA vs. a generic memory chip maker.)

**Gate 3 · Is the market pricing this incorrectly?**
This gate uses a quantitative formula — not an opinion. It scores the company's valuation relative to similar companies, institutional positioning gaps, and whether the market is using the wrong narrative to value it. (Example: Alphabet priced as an ad company while becoming an AI computing platform.)

**Gate 4 · Does this position make the portfolio safer or more dangerous?**
Gate 4 runs a factor analysis — does this new position increase our dependence on a single theme (like AI chip manufacturing in Taiwan) beyond safe limits? If it does, we cannot add the position without simultaneously reducing another.

**Gate 5 · Is this the right time?**
This gate is fully automated. In DEFENSIVE regime, new positions are blocked and queued. In CRASH regime, nothing new enters. The system will not override this gate regardless of how attractive the opportunity looks. Timing discipline is not optional.

**Gate 6 · What do you know and how do you know it?**
The only human gate. The PM must declare the source of their insight: direct conversation (highest value), pattern recognition from prior cycles (high value), or public synthesis (lower value — requires higher Gate 3 score). Gut feelings are not a valid source category.

## The Daily Flow — What Happens Every Day
ARMS does not sleep. Markets move twenty-four hours a day. Geopolitical events happen at 3am. Oil prices shift before New York opens. ARMS processes all of it continuously. Below is the flow of a typical day.

* **All night (Data ingestion):** ARMS continuously monitors market signals. The regime score updates every five minutes.
* **5:15 AM CT (Portfolio snapshot):** Precise reading of every position, weight, and status.
* **5:20 AM CT (Module sweep):** All seven pillars run simultaneously.
* **5:30 AM CT (Daily monitor compiled):** Complete daily report assembled as a digital document.
* **6:00 AM CT (Monitor delivered):** Received by PM and GPs. No human assembled it.
* **Market open (9:30) (Live execution mode):** Tier 0 actions execute automatically. No human required.
* **During market hours (Continuous monitoring):** If something requires action, it acts (Tier 0) or notifies the PM (Tier 1) immediately.
* **Weekly (Monday) (Scan Engine runs):** Screens the AI infrastructure universe against Gates 1 & 2.
* **Monthly (1st) (Learning loop runs):** System scores its own past decisions and adjusts accordingly.

## What Humans Do — And What They Do Not
The PM does the one thing no algorithm can replicate: he sees the future before it is in the data. His job is to identify what the world will look like before the market prices it in.

**The PM does this:**
* Identifies companies that represent civilizational shifts.
* Brings pattern recognition from lived experience.
* Seeds new SENTINEL analyses with a thesis.
* Declares the source of the insight.
* Reviews and confirms/vetoes Tier 1 recommendations.
* Builds and maintains LP/investment community relationships.
* Holds strategic vision.

**The PM does NOT do this:**
* Set position sizes — MICS does this.
* Execute trades — execution layer does this.
* Decide when to deleverage — ARAS and PDS do this.
* Override the regime ceiling — requires GP co-sign.
* Decide when to re-enter — ARES manages re-entry.
* Manage the tail hedge — PTRH manages this.
* Make gut-feel decisions under pressure.

## What Makes Achelion Different — The Honest Answer
Every hedge fund tells LPs they have a disciplined process. What they mean is that their PM has good intentions and tries to be disciplined. ARMS makes the discipline structural.

* **Every sizing decision is derived from a formula, not an opinion.**
* **The regime ceiling cannot be overridden by the PM alone.**
* **Every decision is logged with the reason it was made.**
* **The defensive architecture was validated through the worst tech year since 2000.** (2022 backtest: -16.1% vs Nasdaq-100's -32.6%).
* **The PM's job is to see the future — not to manage the process.**

## Questions GPs Will Hear — Suggested Responses
* **"What happens when the system is wrong?"** ARMS fails gracefully. The structural safeguards (PTRH, PDS, defensive sleeve) still apply. Most funds fail catastrophically because there is no architecture, just a PM who was wrong.
* **"What if the AI makes a bad decision?"** ARMS enforces rules, it does not make discretionary trade decisions. "AI" is the analytical layer for thesis evaluation, not an autonomous agent blindly trading capital.
* **"What does the PM actually do?"** He provides vision. The system provides execution.
* **"How is this different from a quant fund?"** Quant funds trade historical data patterns. We invest in the next era of global infrastructure, using systemic discipline to stay invested correctly and protect capital.
* **"What is your track record?"** Full-cycle backtest (2020-2022) showing +47.4% vs S&P 500's +24.8%, and strong capital preservation in 2022.
* **"Can I see the system running?"** Yes, we share the automated daily monitor during due diligence.

## In Summary
ARMS is not a feature. It is the fund.

The Wall Street model is built on trust in individuals. Achelion is built on trust in architecture. We believe the LP who understands this distinction — who recognizes that the system cannot panic, cannot fall in love with a position, cannot rationalize holding something that should be sold, cannot be tired at 2am when a geopolitical event moves markets — will find that distinction deeply reassuring.

We are not asking LPs to trust our PM's judgment in the moment. We are asking them to evaluate the quality of the architecture we built before the moment arrived.

> *Far more money has been lost on Wall Street by investors who believed in salesmen than by investors who believed in systems. We built a system. Come and inspect it.*
>
> *"Silence is trust in the architecture."*
> 
> Achelion Capital Management, LLC
> Flow. Illumination. Discipline. Conviction.
