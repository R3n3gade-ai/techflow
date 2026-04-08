"""
ARMS Data Feeds: Crypto Plugin (live public REST implementation)

Fetches crypto microstructure proxies from public endpoints instead of
returning fabricated values. If a source cannot be fetched, the plugin
returns only the signals it could source successfully.
"""

import datetime
import json
from typing import List
from urllib.request import Request, urlopen

from data_feeds.interfaces import FeedPlugin, SignalRecord


class CryptoPlugin(FeedPlugin):
    @property
    def name(self) -> str:
        return "CRYPTO_SENSES"

    def _fetch_json(self, url: str, timeout: int = 15):
        req = Request(url, headers={"User-Agent": "Achelion-ARMS/1.0"})
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def fetch(self) -> List[SignalRecord]:
        print(f"[{self.name} Plugin] Fetching live crypto microstructure proxies...")
        records: List[SignalRecord] = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Binance funding rates (public)
        funding_specs = [
            ("BTCUSDT", "BTC_FUNDING", "BTC"),
            ("SOLUSDT", "SOL_FUNDING", "SOL"),
        ]
        for symbol, signal_type, ticker in funding_specs:
            try:
                payload = self._fetch_json(
                    f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1"
                )
                if payload:
                    raw_value = float(payload[-1]["fundingRate"])
                    normalized_value = max(0.0, min(1.0, (raw_value + 0.001) / 0.002))
                    records.append(SignalRecord(
                        ticker=ticker,
                        signal_type=signal_type,
                        value=normalized_value,
                        raw_value=raw_value,
                        source=self.name,
                        timestamp=payload[-1].get("fundingTime", now),
                        cost_tier='FREE'
                    ))
            except Exception as e:
                print(f"[{self.name} Plugin] Funding fetch failed for {symbol}: {e}")

        # Binance open interest snapshot (public)
        oi_specs = [
            ("BTCUSDT", "BTC_OI", "BTC"),
            ("SOLUSDT", "SOL_OI", "SOL"),
        ]
        for symbol, signal_type, ticker in oi_specs:
            try:
                payload = self._fetch_json(
                    f"https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}"
                )
                raw_value = float(payload["openInterest"])
                normalized_value = 0.5  # Placeholder scale until OI regime bands are specified.
                records.append(SignalRecord(
                    ticker=ticker,
                    signal_type=signal_type,
                    value=normalized_value,
                    raw_value=raw_value,
                    source=self.name,
                    timestamp=now,
                    cost_tier='FREE'
                ))
            except Exception as e:
                print(f"[{self.name} Plugin] Open interest fetch failed for {symbol}: {e}")

        # Stablecoin pegs from Coinbase spot as a public proxy.
        peg_specs = [
            ("USDT-USD", "USDT_PEG"),
            ("USDC-USD", "USDC_PEG"),
            ("DAI-USD", "DAI_PEG"),
        ]
        for product_id, signal_type in peg_specs:
            try:
                payload = self._fetch_json(f"https://api.exchange.coinbase.com/products/{product_id}/ticker")
                raw_value = float(payload["price"])
                normalized_value = max(0.0, min(1.0, (raw_value - 0.95) / 0.10))
                records.append(SignalRecord(
                    ticker="GEOPOL",
                    signal_type=signal_type,
                    value=normalized_value,
                    raw_value=raw_value,
                    source=self.name,
                    timestamp=payload.get("time", now),
                    cost_tier='FREE'
                ))
            except Exception as e:
                print(f"[{self.name} Plugin] Stablecoin peg fetch failed for {product_id}: {e}")

        print(f"[{self.name} Plugin] Live fetch complete. Returning {len(records)} records.")
        return records


if __name__ == '__main__':
    plugin = CryptoPlugin()
    for r in plugin.fetch():
        print(f"{r.signal_type}: {r.raw_value} (Normalized: {r.value})")
