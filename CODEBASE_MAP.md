### Achelion ARMS: Codebase Map & Architecture

```
achelion_arms/
│
├── 📄 CODEBASE_MAP.md              # This file: A visual map of the entire project.
├── 📄 PROJECT_PLAN.md              # Our master build plan and task list, broken down by phase.
│
├── 📁 docs/                         # Contains all the detailed specification and strategy documents.
│   ├── 📄 Addendum_1_ARMS_Module_Spec_PTRH_DSHP_v1.0.md
│   ├── 📄 Addendum_2_ARMS_Module_Spec_CDM_TDC_v1.0.md
│   ├── 📄 Addendum_3_ARMS_Intelligence_Architecture_Phase2_3_v1.0.md
│   ├── 📄 ARMS_EOD_Snapshot_Spec_v1.0.md
│   ├── 📄 ARMS_FSD_Master_Build_Document_v1.1.md
│   └── 📄 ARMS_GP_Briefing_v1.0.md
│
├── 📁 monitor_examples/            # The visual mock-up images for the daily report UI.
│   ├── 🖼️ monitor_01_decision_queue.png
│   └── 🖼️ ... (8 other images)
│
└── 📁 src/                         # The main folder for all of our working Python code.
    │
    ├── 🐍 __init__.py              # Makes 'src' a usable code package.
    ├── 🐍 main.py                  # The "Ignition Switch": The main file that runs the entire system.
    │
    ├── 📁 data_feeds/              # 🧠 THE SENSES: Connects ARMS to the outside world for data.
    │   ├── 🐍 __init__.py
    │   ├── 🐍 interfaces.py        # Defines the standard "plug" for any sensor we build.
    │   ├── 🐍 pipeline.py          # The "computer" that gathers data from all connected sensors.
    │   └── 🐍 fred_plugin.py       # Our first sensor, for reading economic data from the Federal Reserve.
    │
    ├── 📁 engine/                  # 🧠 THE BRAIN: Where all decisions, analysis, and learning happen.
    │   ├── 🐍 __init__.py
    │   ├── 🐍 mics.py              # The core logic: Calculates position size based on data, not opinion.
    │   ├── 🐍 session_log_analytics.py # The "learning" module that reviews past decisions to get smarter.
    │   └── 🐍 systematic_scan.py   # The "proactive scout" that automatically finds new investment ideas.
    │
    ├── 📁 execution/               # 🧠 THE NERVES & MUSCLES: Turns the brain's decisions into market actions.
    │   ├── 🐍 __init__.py
    │   ├── 🐍 interfaces.py        # Defines the standard "nerve signals" (OrderRequest) for all actions.
    │   ├── 🐍 broker_api.py        # The "muscle" that connects to Interactive Brokers to place trades.
    │   └── 🐍 confirmation_queue.py # The secure "inbox" for the few actions that require your final approval.
    │
    └── 📁 reporting/               # 🧠 THE MEMORY & VOICE: Records history and creates reports.
        ├── 🐍 __init__.py
        └── 🐍 audit_log.py         # The system's un-editable "memory" or "trip log" for a perfect audit trail.
```