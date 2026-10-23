# Research & Architectural Decisions: FoodLoop

## 1. Multi-Agent Orchestration Architecture

### Options Considered
- **Option A: Pure sequential scripts**: Simple, but brittle and lacks modular agent boundaries.
- **Option B: LangGraph / Google ADK StateGraph (Selected)**: State machine pattern representing the food rescue lifecycle (`Intake` -> `SafetyEngine` -> `MatchingEngine` -> `LogisticsEngine`). Provides deterministic transitions, checkpointing, and easy observability.

### Decision
Adopt a lightweight async StateGraph pattern inspired by Google ADK / LangGraph:
- `IntakeAgent`: Multimodal extraction via Vertex AI Gemini 2.5 Flash with strict Pydantic JSON schema constraints.
- `SafetyAgent`: Deterministic FSSAI rule engine first; Gemini Pro auxiliary reasoning for edge cases and plain-language explanation generation.
- `MatchingAgent`: In-memory spatial index + multi-objective ranking algorithm calculating composite fit scores for candidate NGOs.
- `LogisticsAgent`: Proximity matching with volunteer dispatch and Google Maps Directions API routing.

---

## 2. Model Selection & Vertex AI Strategy

| Agent | Model | Justification | Latency Target |
| :--- | :--- | :--- | :--- |
| **Intake (Multimodal)** | Gemini 2.5 Flash | High throughput, multimodal image/audio reasoning, sub-second TTFT, low cost. | < 2.5s |
| **Safety Engine** | Deterministic Python + Gemini 2.5 Flash | Zero hallucination on threshold temperatures and holding hours. Gemini explains reasoning. | < 1.0s |
| **Matching Engine** | Deterministic Ranking + Gemini 2.5 Flash | Mathematical scoring for strict fairness; LLM generates contextual match rationales. | < 1.5s |
| **Surplus Forecaster**| BigQuery ML (ARIMA+ / Linear Reg) | Cloud data warehouse native predictive modeling without extra infrastructure. | Async |

---

## 3. Security, Prompt Defense & Privacy

- **Prompt-Injection Defense**: User descriptions, OCR text, and voice transcriptions are treated as untrusted data inputs. They are passed strictly inside typed JSON input fields of system prompts, preceded by boundary instructions (`<UNTRUSTED_CONTENT>...</UNTRUSTED_CONTENT>`), preventing instruction override.
- **PII Redaction**: Regex + lightweight NER pipeline masks phone numbers (`\+?[0-9]{10,12}` -> `[PHONE_MASKED]`) and precise flat/house numbers prior to calling Gemini APIs and prior to mutual match confirmation.
- **Role-Based Custom Claims**: Firebase Auth JWT claims specify `role: "donor" | "ngo" | "volunteer" | "admin"`. Backend middleware and Firestore security rules validate these tokens.

---

## 4. Performance & Caching Strategy

- **Geospatial Distance Caching**: Pre-calculate and cache donor-to-NGO Euclidean distances in Redis / memory LRU before calling Google Distance Matrix API for final top-3 candidates.
- **Streaming & Async Handlers**: FastAPI async routes decouple ingestion from BigQuery streaming inserts via background tasks / Google Cloud Pub/Sub.
- **Client PWA**: Optimistic UI updates with Firestore client-side offline persistence.
