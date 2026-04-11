# src/data_feeds/pipeline.py
# The main orchestrator for the data ingestion pipeline.

import os
from typing import List

from .interfaces import FeedPlugin, SignalRecord
from .fred_plugin import FredPlugin
from .crypto_plugin import CryptoPlugin
from .pmi_plugin import PmiPlugin

STRICT_LIVE_MODE = os.environ.get('ARMS_STRICT_LIVE', '1').strip().lower() not in {'0', 'false', 'no'}

class DataPipeline:
    """
    Initializes and runs all available data feed plugins.
    
    NOTE: This pipeline follows the "receptor" pattern from FSD v1.1.
    New plugins (e.g., SecEdgarPlugin) will be added here as they are developed.
    """
    
    def __init__(self):
        # In strict live mode, critical regime inputs must be present and sourced.
        self.plugins: List[FeedPlugin] = [FredPlugin(), CryptoPlugin(), PmiPlugin()]
        print(f"[DataPipeline] Initialized with {len(self.plugins)} specified plugin(s). Strict={STRICT_LIVE_MODE}")

    def run_all_feeds(self) -> List[SignalRecord]:
        """
        Runs the fetch() method on all initialized plugins and aggregates
        their results into a single list of SignalRecords.
        """
        all_signals = []
        print(f"[DataPipeline] Running {len(self.plugins)} feed(s)...")
        failures = []
        for plugin in self.plugins:
            try:
                signals = plugin.fetch()
                all_signals.extend(signals)
                print(f"[DataPipeline]   - {plugin.name}: OK, returned {len(signals)} record(s).")
            except Exception as e:
                print(f"[DataPipeline]   - {plugin.name}: FAILED with error: {e}")
                failures.append((plugin.name, str(e)))

        if STRICT_LIVE_MODE and failures:
            joined = "; ".join([f"{name}: {err}" for name, err in failures])
            raise RuntimeError(f"Strict live data pipeline failed: {joined}")
        
        print(f"[DataPipeline] Run complete. Total records fetched: {len(all_signals)}")
        return all_signals
