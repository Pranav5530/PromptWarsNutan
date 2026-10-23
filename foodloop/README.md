# FoodLoop: Autonomous Surplus Food Rescue Multi-Agent Platform

FoodLoop is an AI-powered, multi-agent surplus food rescue platform connecting food donors (restaurants, caterers, university mess halls) with nearby NGOs and volunteers in real-time. Built for urban centers with high food-surplus density, FoodLoop guarantees listing-to-match dispatch in under 60 seconds with strict zero-tolerance deterministic food-safety verification.

---

## 🏆 Hackathon Judging Criteria Alignment

| Judging Dimension | Architecture & Implementation Highlight |
| :--- | :--- |
| **Security** | Role-Based Access Control (`donor`, `ngo`, `volunteer`, `admin`), Firestore least-privilege security rules, App Check, Secret Manager, PII masking, and multimodal prompt injection defense layer. |
| **Efficiency** | In-memory spatial index, distance calculation caching, streamed BigQuery inserts, sub-60-second listing-to-match SLA, capped token budgets. |
| **Technology Implemented** | Multi-Agent StateGraph architecture (`IntakeAgent`, `SafetyAgent`, `MatchingAgent`, `LogisticsAgent`), deterministic FSSAI safety rules engine, BigQuery ML surplus hotspot forecasting. |
| **Performance** | Asynchronous FastAPI on Cloud Run, sub-second TTFT Gemini 2.5 Flash intake, PWA mobile client with offline optimistic caching. |
| **Google Technology Used** | Gemini 2.5 Flash & Pro via Vertex AI, Firebase Suite (Auth, Firestore, Cloud Storage, Hosting, App Check), Cloud Run, Google Secret Manager, BigQuery & BigQuery ML, Google Maps Platform APIs. |

---

## 📦 Disclosed Open-Source Libraries, APIs & Google Technologies

### Google Technologies & APIs
1. **Google Vertex AI (Gemini 2.5 Flash & Gemini Pro)**: Multimodal intake extraction, safety explanation generation, and match rationale synthesis.
2. **Firebase Suite**:
   - **Firebase Authentication**: User identity with custom claims for RBAC.
   - **Cloud Firestore**: Real-time operational database and security rules.
   - **Cloud Storage**: Food photos, audio recordings, and proof of delivery images.
   - **Firebase App Check**: Client endpoint protection against abuse.
   - **Firebase Hosting**: High-speed PWA static hosting.
3. **Google Cloud Run**: Serverless container execution for FastAPI backend agents.
4. **Google Cloud Secret Manager**: Production API key and credentials isolation.
5. **Google BigQuery & BigQuery ML**: Real-time event streaming, impact aggregation, and surplus hotspot time-series forecasting.
6. **Google Maps Platform (JS API & Directions)**: Spatial routing, turn-by-turn volunteer navigation, and interactive shelter mapping.

### Open-Source Python & Node Libraries
- **FastAPI**: Modern, asynchronous Python web framework for agent endpoints.
- **Pydantic & Pydantic-Settings**: Strict data validation and settings management.
- **Uvicorn**: High-performance ASGI server.
- **HTTPX**: Async HTTP client for external integrations.
- **Pytest & Pytest-Asyncio**: Unit testing, agent contract testing, and 30-sample evaluation suite.
- **Python-Jose**: Cryptographic JWT validation for custom role claims.
- **Next.js 15 & React 19**: Frontend Progressive Web App (PWA).
- **Tailwind CSS**: Modern utility-first responsive interface design.

---

## 🚀 Quickstart & Running Tests

### 1. Run Complete Test & Evaluation Suite
```bash
cd backend
uv run pytest -v
```

This runs:
- `test_auth_roles.py`: Role-based access control and token verification.
- `test_intake_schemas.py`: PII redaction and multimodal prompt injection defenses.
- `test_safety_rules.py`: Deterministic FSSAI temperature/holding time rules.
- `test_matching_agent.py`: Proximity, dietary filtering, and capacity scoring.
- `test_logistics.py`: Volunteer assignment and Proof of Delivery.
- `test_bigquery_pipeline.py`: BigQuery event streaming and impact metrics.
- `test_evaluation_suite.py`: Benchmark running against all 30 evaluation food samples.

### 2. Run Demo Data Seeder
```bash
cd backend
uv run python -m app.scripts.seed_demo_data
```

### 3. Start Local Agent API Server
```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```
Interactive Swagger API documentation is available at `http://localhost:8000/docs`.

---

## 🛡️ Food Safety & Evaluation Benchmark

The system includes a dedicated 30-sample evaluation benchmark (`backend/tests/data/eval_listings.json`) covering cooked meals, bakeries, desserts, high-ambient-heat scenarios (>32°C), expired holding times, allergen edge cases, and adversarial prompt injections.

- **Deterministic Safety Guarantee**: Zero unsafe or expired food listings can ever receive an auto-approved `Safe` verdict.
- **Benchmark Accuracy**: >= 90% alignment with ground-truth food safety classifications.
