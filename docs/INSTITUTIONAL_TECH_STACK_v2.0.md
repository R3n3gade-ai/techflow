# The Institutional Tech Stack (The Fortress) v2.0

## Performance Target: <30-Second Latency
To guarantee the **<30-second latency targets** for **Intraday Circuit Breakers (SYS-1)** and the **15-45 minute Kill Chain**, ARMS utilizes a modern, async-first, highly available cloud architecture. All components are selected for institutional-grade reliability and security.

---

### 1. Core Engine (Backend)
- **Runtime:** **Python 3.11+** (Async-native implementation).
- **Communication:** **FastAPI** for high-performance async API and WebSocket endpoints.
- **Orchestration:** **Prefect** (or Celery on ECS) for robust task scheduling of the **5-min RPE loops**, **Monday 6 AM Scan Engine**, and daily monitors.

### 2. Mathematics & Data Processing
- **Libraries:** **pandas**, **numpy**, and **scipy**.
- **Calculations:** Powers the z-score normalization, MAE (Mean Absolute Error) regressions for the **PMI Nowcast**, and **MICS (Conviction-Squared)** position sizing.

### 3. Relational Database (State & Audit)
- **Engine:** **PostgreSQL** (Managed via RDS).
- **ORM:** **SQLAlchemy** & **psycopg2**.
- **Responsibility:** Persistent storage for the **immutable audit_log**, portfolio snapshots, order books, and historical PMI/Regime transitions.

### 4. In-Memory Cache (High-Speed Signals)
- **Engine:** **Redis** (Managed via ElastiCache).
- **Responsibility:** Crucial for **SYS-1 (Circuit Breakers)** and **SYS-5 (Correlation Monitor)**. Tick data for rolling 1-hour crypto/equity correlations is held in RAM to ensure sub-second computation.

### 5. Intelligence & Vector Memory
- **Provider:** **Pinecone** or **AWS OpenSearch**.
- **LLM Integration:** **Anthropic Claude 3.5/4.0** API.
- **Responsibility:** Stores SEC EDGAR filings and earnings transcript embeddings for the **SENTINEL Systematic Scan Engine**.

### 6. PM Control Room (Frontend)
- **Framework:** **Tauri + React + TypeScript**.
- **Architecture:** A secure, compiled desktop application that communicates with "The Fortress" via encrypted WebSockets.
- **Features:** Real-time dashboards, the **3-option Confirmation Queue**, and PM overrides for MICS/Regime assessment.

### 7. Cloud Infrastructure (AWS "The Fortress")
- **Compute:** **ECS (Fargate)** for containerized orchestration of the Master Engine.
- **Security:** **AWS Secrets Manager** for API keys; **IAM** with least-privilege access; **VPC** with private subnets.
- **Governance:** **Zero Local Execution.** All critical logic runs in the cloud to ensure 100% uptime and an unbroken audit trail.
