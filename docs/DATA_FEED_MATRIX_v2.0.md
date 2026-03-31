# Comprehensive Data Feed Matrix v2.0

## Intelligence Architecture: The 7-Layer Feed
To feed the ARMS 7-layer architecture without overlap, we utilize a modular **FeedPlugin** interface. This allows us to swap vendors or upgrade from free to institutional-grade feeds without re-architecting the ingestion engine.

---

### 1. Macro Compass & ARAS M1 (Macro/Liquidity)
*Status: FRED Plugin Active. PMI Nowcast Pending.*
- **FRED API (Free):** 
    - **Liquidity:** Reverse Repo (RRP), Bank Reserves, TGA, Fed Balance Sheet.
    - **Credit:** HY OAS, IG OAS.
    - **Rates/Macro:** DGS10, DXY, CPI.
    - **Sentiment:** ICI Equity Fund Flows, Household Equity Alloc (Fed Z.1).
- **S&P Global PMI (Subscription/Terminal):** 
    - Flash & Final US Manufacturing PMI.
    - **Note:** Formally replaces ISM. Requires dual-layer live/nowcast blending as per PMI Module Spec v1.0.

### 2. Crypto Intelligence (Market Microstructure)
*Status: Planning Phase.*
- **Exchange APIs (Binance / Bybit / OKX - Free):** 
    - Real-time BTC & SOL funding rates.
    - Open Interest (OI) and Long/Short ratios.
- **CoinGlass API (Free/Tiered):** 
    - 24hr Liquidation volumes (Critical for ARAS M2 - Liquidations/Capitulation).
- **CoinGecko (Free):** 
    - Stablecoin pegs (USDT, USDC, DAI) for ARAS M6 (Shutdown/De-peg Risk).

### 3. Equities, Options & Gamma (Market Mechanics)
*Status: IBKR Integration Active.*
- **Interactive Brokers (IBKR):** 
    - Primary source for real-time QQQ, IBIT, VIX, and portfolio equity pricing.
- **Gamma Edge / Market Mechanics:** 
    - **Net GEX, Gamma Flip, Call/Put Walls.**
    - **Note:** Prioritizing integration of free/broker-provided data via Gamma Edge or custom calculation over external $200/mo subscriptions (SpotGamma). Required for ARAS M4 (Dealer Gamma).
- **CBOE / Options Data:** 
    - VIX Term Structure (VIX3M), Put/Call ratios, 25-Delta Risk Reversals.
- **CME Group:** 
    - S&P 500 Futures (ES) for SYS-4 Overnight Monitoring and Gap Analysis.

### 4. Retail Sentiment - MC-RSS (Sentiment)
*Status: Phase 2/3.*
- **VandaTrack (Subscription):** 
    - Daily retail net buying flows (The anchor for MC-RSS).
- **Survey Data (Free/Scraped):** 
    - AAII (Retail Sentiment) and NAAIM (Active Manager Exposure) for contrarian overrides.

### 5. Intelligence Layer (Narrative & Analysis)
*Status: Active (Claude Integration).*
- **Anthropic API (Claude 3.5 Sonnet/Opus):** 
    - Powers the **Systematic Scan Engine**, **SENTINEL Gate 1 & 2** analysis, and automated LP Narratives.
- **SEC EDGAR (Free):** 
    - Automated pulls of 10-K, 10-Q, 8-K filings and earning transcripts for intelligence briefs.

---

## Technical Implementation
All feeds are processed through `src/data_feeds/pipeline.py`. 
- **Tier 0:** Automated ingestion and normalization.
- **Tier 1:** Validation required for data integrity (PM approval of feed status/health).
