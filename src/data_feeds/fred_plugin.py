# src/data_feeds/fred_plugin.py
# A concrete implementation of a FeedPlugin for the FRED data source.

from datetime import datetime
from typing import List

from .interfaces import FeedPlugin, SignalRecord

# A list of specific economic series we want to track from FRED.
# This would be expanded and likely moved to a configuration file.
FRED_SERIES_IDS = {
    "FED_FUNDS_RATE": "FEDFUNDS",
    "10Y_TREASURY_YIELD": "DGS10",
    "VIX_INDEX": "VIXCLS",
}

class FredPlugin(FeedPlugin):
    """
    A FeedPlugin to fetch key economic indicators from the
    Federal Reserve Economic Data (FRED) API.
    """
    
    @property
    def name(self) -> str:
        return "FRED"

    def fetch(self) -> List[SignalRecord]:
        """
        Fetches the latest data for the configured series from the FRED API.
        
        NOTE: This is a SIMULATED response for testing purposes, as we are
        not making live API calls from this environment.
        """
        
        print(f"[{self.name} Plugin] Generating SIMULATED data from FRED...")
        
        records = []
        now = datetime.utcnow().isoformat()
        
        # --- Simulated Logic ---
        # This block simulates what would be returned from live API calls.
        simulated_data = {
            "FED_FUNDS_RATE": "5.33",
            "10Y_TREASURY_YIELD": "4.25",
            "VIX_INDEX": "13.5",
        }

        for signal_type, raw_value in simulated_data.items():
            value = float(raw_value)
            # Placeholder for normalization logic
            normalized_value = value / 100 if "RATE" in signal_type else value / 100 # Simple example

            records.append(SignalRecord(
                ticker="MACRO",
                signal_type=signal_type,
                value=normalized_value,
                raw_value=raw_value,
                source=self.name,
                timestamp=now,
                cost_tier='FREE'
            ))
        
        print(f"[{self.name} Plugin] Simulated fetch complete. Returning {len(records)} records.")
        return records

