"""
ARMS Configuration: Systematic Scan Engine Universe

This file defines the universe of companies to be scanned weekly by the
Systematic Scan Engine. The engine will evaluate each company against
SENTINEL Gates 1 and 2.

The universe is focused on AI infrastructure and enabling technologies.
This list is maintained by the PM.

Reference: arms_fsd_master_build_v1.1.md, Section 11.3
"""

# The universe is a simple list of ticker symbols.
SCAN_UNIVERSE = [
    # Semiconductors (Fabless & Foundry)
    "NVDA", "AMD", "AVGO", "QCOM", "MRVL", "TSM", "INTC", "MU",
    
    # AI Infrastructure & Networking
    "ANET", "SMCI", "DELL", "HPE", "VRT", "ETN", "MSFT", "GOOGL", "AMZN", "META",
    
    # EDA & IP
    "CDNS", "SNPS", "ARM",
    
    # Other Enabling Tech
    "ALAB", "PLTR"
]
