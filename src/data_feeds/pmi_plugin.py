"""
ARMS Data Feeds: S&P Global PMI Plugin

Production rule: do not emit fabricated PMI values.
Supported temporary bridge sources:
1. JSON endpoint via ARMS_PMI_URL
2. Local CSV/Excel-export-style file via ARMS_PMI_CSV
"""

import csv
import datetime
import json
import os
from typing import List, Optional
from urllib.request import Request, urlopen

from data_feeds.interfaces import FeedPlugin, SignalRecord
from engine.bridge_paths import bridge_path


class PmiPlugin(FeedPlugin):
    @property
    def name(self) -> str:
        return "SP_GLOBAL_PMI"

    def _fetch_json(self, url: str, timeout: int = 15):
        req = Request(url, headers={"User-Agent": "Achelion-ARMS/1.0"})
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def _read_csv_latest(self, path: str) -> Optional[SignalRecord]:
        latest_row = None
        with open(path, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_val = (row.get('Date') or row.get('date') or '').strip()
                value_val = (row.get('Value') or row.get('value') or '').strip()
                if not date_val or not value_val:
                    continue
                if latest_row is None or date_val > latest_row['date']:
                    latest_row = {'date': date_val, 'value': value_val}

        if latest_row is None:
            return None

        raw_value = float(latest_row['value'])
        return SignalRecord(
            ticker="MACRO",
            signal_type="PMI_NOWCAST",
            value=raw_value / 100.0,
            raw_value=raw_value,
            source=self.name,
            timestamp=latest_row['date'],
            cost_tier='INSTITUTIONAL'
        )

    def fetch(self) -> List[SignalRecord]:
        records: List[SignalRecord] = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        source_url = os.environ.get("ARMS_PMI_URL")
        source_csv = os.environ.get("ARMS_PMI_CSV") or bridge_path('ARMS_PMI_CSV', 'pmi_latest.csv')

        if source_url:
            print(f"[{self.name} Plugin] Fetching PMI from configured URL source...")
            try:
                payload = self._fetch_json(source_url)
                raw_value = float(payload["pmi_nowcast"])
                records.append(SignalRecord(
                    ticker="MACRO",
                    signal_type="PMI_NOWCAST",
                    value=raw_value / 100.0,
                    raw_value=raw_value,
                    source=self.name,
                    timestamp=str(payload.get("timestamp", now)),
                    cost_tier='INSTITUTIONAL'
                ))
            except Exception as e:
                print(f"[{self.name} Plugin] Failed to fetch configured PMI URL source: {e}")

        elif source_csv:
            print(f"[{self.name} Plugin] Reading PMI from configured CSV source...")
            try:
                record = self._read_csv_latest(source_csv)
                if record:
                    records.append(record)
            except Exception as e:
                print(f"[{self.name} Plugin] Failed to read configured PMI CSV source: {e}")
        else:
            print(f"[{self.name} Plugin] No ARMS_PMI_URL or ARMS_PMI_CSV configured. Skipping PMI feed.")

        print(f"[{self.name} Plugin] Fetch complete. Returning {len(records)} records.")
        return records


if __name__ == '__main__':
    plugin = PmiPlugin()
    for r in plugin.fetch():
        print(f"{r.signal_type}: {r.raw_value} (Normalized: {r.value})")
