"""
ARMS Module: Customer Dependency Map (CDM) Engine

This module provides the cross-sector signal propagation layer for ARMS.
It scans incoming data (news, filings) for named entities defined in the
dependency map and propagates alerts to all positions that depend on those
entities.

This is the "data layer" for the Thesis Dependency Checker (TDC).

Reference: ARMS Module Specification — CDM + TDC | Addendum 2 to FSD v1.1
"""

from dataclasses import dataclass, field
from typing import List, Dict, Literal
import sys
import os
from datetime import datetime

# Add the config directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))

from position_dependency_map import POSITION_DEPENDENCIES, ALERT_SENSITIVITY_MAPPING

# --- Data Structures ---

@dataclass
class NewsItem:
    """Represents a single piece of incoming data to be scanned."""
    source: str  # e.g., 'SEC_EDGAR', 'NewsAPI'
    headline: str
    content: str
    timestamp: str
    entities: List[str]  # Pre-processed named entities found in the content
    event_type: Literal[
        'LEGAL_RULING', 'REGULATORY_FILING', 'EARNINGS_WARNING', 'MA_ANNOUNCEMENT',
        'INSIDER_SALE', 'LEADERSHIP_CHANGE', 'CREDIT_EVENT', 'PARTNERSHIP_CHANGE',
        'PRODUCT_DELAY', 'POSITIVE_DEVELOPMENT', 'UNKNOWN'
    ]

@dataclass
class CdmAlert:
    """Represents a single alert propagated to a dependent position."""
    ticker: str
    triggering_entity: str
    event_type: str
    severity: Literal['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    headline: str
    source_item: NewsItem
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

# --- CDM Engine Logic ---

def find_dependent_tickers(entity: str) -> List[str]:
    """Finds all tickers in the map that depend on the given entity."""
    affected_tickers = []
    normalized_entity = entity.lower()
    
    for ticker, dependencies in POSITION_DEPENDENCIES.items():
        all_deps = (
            dependencies.get('primary_demand_drivers', []) +
            dependencies.get('thesis_enablers', []) +
            dependencies.get('regulatory_counterparties', [])
        )
        if any(normalized_entity in dep.lower() for dep in all_deps):
            affected_tickers.append(ticker)
            
    return affected_tickers

def run_cdm_scan(news_items: List[NewsItem]) -> List[CdmAlert]:
    """
    Scans a list of news items and generates CDM alerts for dependent positions.
    """
    all_alerts = []
    for item in news_items:
        if item.event_type == 'POSITIVE_DEVELOPMENT' or item.event_type == 'UNKNOWN':
            continue # Per spec, positive/unknown events do not generate alerts

        for entity in item.entities:
            dependent_tickers = find_dependent_tickers(entity)
            
            for ticker in dependent_tickers:
                sensitivity = POSITION_DEPENDENCIES[ticker]['alert_sensitivity']
                triggering_events = ALERT_SENSITIVITY_MAPPING.get(sensitivity, [])
                
                if item.event_type in triggering_events:
                    severity = sensitivity # For simplicity, alert severity matches position sensitivity
                    if item.event_type == 'LEGAL_RULING': # Per spec, this is CRITICAL
                        severity = 'CRITICAL'

                    alert = CdmAlert(
                        ticker=ticker,
                        triggering_entity=entity,
                        event_type=item.event_type,
                        severity=severity,
                        headline=item.headline,
                        source_item=item
                    )
                    all_alerts.append(alert)
                    # TODO: Integrate with audit log
                    print(f"AUDIT LOG: CDM Alert Generated: {ticker} <-- {entity} ({item.event_type})")

    return all_alerts

# This file is intended to be imported as a module.
# The test cases have been moved to tests/test_cdm_tdc.py
