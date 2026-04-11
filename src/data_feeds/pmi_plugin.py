"""
ARMS Data Feeds: S&P Global / ISM PMI Plugin

Production rule: do not emit fabricated PMI values.
Fetches live S&P Global / ISM PMI macro data via public scraping if API 
is not available, fulfilling the FSD "Priority 1" requirement.
"""

import os
import requests
import json
import datetime
from typing import List

from data_feeds.interfaces import FeedPlugin, SignalRecord

STRICT_LIVE_MODE = os.environ.get('ARMS_STRICT_LIVE', '1').strip().lower() not in {'0', 'false', 'no'}

class PmiPlugin(FeedPlugin):
    @property
    def name(self) -> str:
        return "SP_GLOBAL_PMI"

    def fetch(self) -> List[SignalRecord]:
        print(f"[{self.name} Plugin] Fetching live PMI data...")
        records: List[SignalRecord] = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Free API for basic macro indicators
        url = "https://api.tradingeconomics.com/economic-calendar"
        # Since TradingEconomics API is paid, and Investing/S&P blocks scrapers, 
        # we'll build a direct parsing mechanism from the St. Louis Fed's public site
        # since their API blocked ISM but sometimes the HTML page has the headline.
        
        url = "https://fred.stlouisfed.org/series/NAPM"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        raw_val = None
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            
            # The value is usually inside a meta tag or span with class 'series-meta-observation-value'
            import re
            match = re.search(r'class="series-meta-observation-value">\s*([\d\.]+)\s*</span>', r.text)
            if match:
                raw_val = float(match.group(1))
                
            if raw_val is None:
                # Secondary regex search for JSON embedded in the page
                json_match = re.search(r'"observation_value"\s*:\s*"([\d\.]+)"', r.text)
                if json_match:
                    raw_val = float(json_match.group(1))
                    
            if raw_val is not None:
                records.append(SignalRecord(
                    ticker="MACRO",
                    signal_type="PMI_NOWCAST",
                    value=raw_val / 100.0,
                    raw_value=raw_val,
                    source=self.name,
                    timestamp=now,
                    cost_tier='FREE_PROXY'
                ))
                print(f"[{self.name} Plugin] Successfully fetched PMI: {raw_val}")
                return records
                
        except Exception as e:
            print(f"[{self.name} Plugin] Failed to fetch live PMI from FRED: {e}.")
            
        if STRICT_LIVE_MODE:
            raise RuntimeError(f"[{self.name} Plugin] PMI unavailable in strict live mode; refusing stale fallback.")

        # Non-strict fallback mode only.
        print(f"[{self.name} Plugin] Fallback to recent known baseline because strict live mode is disabled.")
        records.append(SignalRecord(
            ticker="MACRO",
            signal_type="PMI_NOWCAST",
            value=0.503,
            raw_value=50.3,
            source=self.name,
            timestamp=now,
            cost_tier='FALLBACK'
        ))

        return records

if __name__ == '__main__':
    plugin = PmiPlugin()
    for r in plugin.fetch():
        print(f"{r.signal_type}: {r.raw_value} (Normalized: {r.value})")
