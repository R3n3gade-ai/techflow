# src/data_feeds/fred_plugin.py
# A concrete implementation of a FeedPlugin for the FRED data source.

import os
from datetime import datetime, timezone
from typing import List, Dict
from urllib.parse import urlencode
from urllib.request import urlopen
import json

STRICT_LIVE_MODE = os.environ.get('ARMS_STRICT_LIVE', '1').strip().lower() not in {'0', 'false', 'no'}

from .interfaces import FeedPlugin, SignalRecord

# A list of specific economic series we want to track from FRED.
# This can be expanded or moved to configuration later.
FRED_SERIES_IDS: Dict[str, str] = {
    "FED_FUNDS_RATE": "FEDFUNDS",
    "10Y_TREASURY_YIELD": "DGS10",
    "VIX_INDEX": "VIXCLS",
    "HY_CREDIT_SPREAD": "BAMLH0A0HYM2",
    # "PMI_NOWCAST": "ISM/MAN_PMI"  # Removed, moving PMI to dedicated plugin  # ISM Manufacturing PMI (used as proxy if S&P Global not available)
}

class FredPlugin(FeedPlugin):
    """
    A FeedPlugin to fetch key economic indicators from the
    Federal Reserve Economic Data (FRED) API.
    """

    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

    @property
    def name(self) -> str:
        return "FRED"

    def _get_api_key(self) -> str:
        api_key = os.environ.get("FRED_API_KEY")
        if not api_key:
            raise RuntimeError("FRED_API_KEY is not set in the environment.")
        return api_key

    def _fetch_latest_observation(self, series_id: str) -> dict:
        params = {
            "series_id": series_id,
            "api_key": self._get_api_key(),
            "file_type": "json",
            "sort_order": "desc",
            "limit": 10,
        }
        url = f"{self.BASE_URL}?{urlencode(params)}"

        with urlopen(url, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))

        observations = payload.get("observations", [])
        for obs in observations:
            value = obs.get("value")
            if value not in (None, "."):
                return obs

        raise RuntimeError(f"No usable observation returned for FRED series {series_id}.")

    def _normalize_value(self, signal_type: str, value: float) -> float:
        if signal_type in {"FED_FUNDS_RATE", "10Y_TREASURY_YIELD", "HY_CREDIT_SPREAD"}:
            return value / 100.0
        if signal_type == "VIX_INDEX":
            return value / 100.0
        if signal_type == "PMI_NOWCAST":
            return value / 100.0
        return value

    def fetch(self) -> List[SignalRecord]:
        """
        Fetch the latest available data for configured FRED series.
        """
        print(f"[{self.name} Plugin] Fetching live data from FRED...")

        records: List[SignalRecord] = []
        fetched_at = datetime.now(timezone.utc).isoformat()

        try:
            api_key = self._get_api_key()
        except RuntimeError as e:
            print(f"[{self.name} Plugin] FAILED with error: {e}")
            raise e

        for signal_type, series_id in FRED_SERIES_IDS.items():
            try:
                obs = self._fetch_latest_observation(series_id)
                raw_value = float(obs["value"])
                normalized_value = self._normalize_value(signal_type, raw_value)
                observation_date = obs.get("date", fetched_at)

                records.append(SignalRecord(
                    ticker="MACRO",
                    signal_type=signal_type,
                    value=normalized_value,
                    raw_value=raw_value,
                    source=self.name,
                    timestamp=observation_date,
                    cost_tier='FREE'
                ))
            except Exception as e:
                message = f"[{self.name} Plugin] Failed to fetch {series_id}: {e}."
                if STRICT_LIVE_MODE:
                    print(message + " Strict live mode forbids synthetic fallback.")
                    raise RuntimeError(f"Critical FRED series unavailable in strict live mode: {series_id}") from e
                print(message + " Using SYNTHETIC fallback (ARMS_STRICT_LIVE=0). These values are NOT market data.")
                fallback_vals = {"FED_FUNDS_RATE": 5.25, "10Y_TREASURY_YIELD": 4.10, "VIX_INDEX": 20.5, "HY_CREDIT_SPREAD": 4.2}
                raw_value = fallback_vals.get(signal_type, 1.0)
                records.append(SignalRecord(
                    ticker="MACRO",
                    signal_type=signal_type,
                    value=self._normalize_value(signal_type, raw_value),
                    raw_value=raw_value,
                    source=f"{self.name}_SYNTHETIC",
                    timestamp=fetched_at,
                    cost_tier='FALLBACK'
                ))

        print(f"[{self.name} Plugin] Live fetch complete. Returning {len(records)} records.")
        return records

