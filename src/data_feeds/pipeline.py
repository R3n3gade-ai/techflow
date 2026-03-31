# src/data_feeds/pipeline.py
# The main orchestrator for the data ingestion pipeline.

from typing import List

from .interfaces import FeedPlugin, SignalRecord
from .fred_plugin import FredPlugin
from .pmi_plugin import PmiPlugin
from .crypto_plugin import CryptoPlugin

class DataPipeline:
    """
    Initializes and runs all available data feed plugins.
    
    NOTE: This pipeline follows the "receptor" pattern from FSD v1.1.
    New plugins (e.g., SecEdgarPlugin) will be added here as they are developed.
    """
    
    def __init__(self):
        # Explicitly list the plugins to load for Phase 1.
        self.plugins: List[FeedPlugin] = [
            FredPlugin(),
            PmiPlugin(),
            CryptoPlugin()
        ]
        print(f"[DataPipeline] Initialized with {len(self.plugins)} specified plugin(s).")

    def run_all_feeds(self) -> List[SignalRecord]:
        """
        Runs the fetch() method on all initialized plugins and aggregates
        their results into a single list of SignalRecords.
        """
        all_signals = []
        print(f"[DataPipeline] Running {len(self.plugins)} feed(s)...")
        for plugin in self.plugins:
            try:
                signals = plugin.fetch()
                all_signals.extend(signals)
                print(f"[DataPipeline]   - {plugin.name}: OK, returned {len(signals)} record(s).")
            except Exception as e:
                print(f"[DataPipeline]   - {plugin.name}: FAILED with error: {e}")
        
        print(f"[DataPipeline] Run complete. Total records fetched: {len(all_signals)}")
        return all_signals
