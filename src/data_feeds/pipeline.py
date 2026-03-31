# src/data_feeds/pipeline.py
# The main orchestrator for the data ingestion pipeline.

from typing import List

from .interfaces import FeedPlugin, SignalRecord
from .fred_plugin import FredPlugin
# As we create more plugins (e.g., SecEdgarPlugin), they will be imported here.

class DataPipeline:
    """
    Initializes and runs all available data feed plugins.
    
    NOTE: The complex plugin discovery logic has been replaced with a simpler,
    hardcoded list of plugins to ensure stability and resolve import issues.
    This is a robust and sufficient approach for the Phase 1 build.
    """
    
    def __init__(self):
        # We explicitly list the plugins to load. This is more stable than
        # dynamic discovery and avoids complex pathing issues.
        self.plugins: List[FeedPlugin] = [
            FredPlugin(),
            # e.g., SecEdgarPlugin() would be added here later
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

# Example of how this would be used by the main ARMS application scheduler:
#
# def scheduled_data_ingestion_task():
#     pipeline = DataPipeline()
#     signals = pipeline.run_all_feeds()
#     process_signals(signals)
