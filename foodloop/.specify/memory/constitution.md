# FoodLoop Constitution

<!-- Hackathon Governance Document: Judged on Security, Efficiency, Technology Implemented, Performance, and Google Technology Used -->

## Core Principles

### I. Security First (NON-NEGOTIABLE)
- **Role-Based Access Control**: Firebase Authentication with custom claims strictly enforces the 4 discrete roles (`donor`, `ngo`, `volunteer`, `admin`).
- **Least-Privilege Data Access**: Firestore Security Rules enforce zero-trust access controls per collection; users can only read/write their own profiles and assigned transactions.
- **API & Asset Protection**: App Check protects client endpoints from abuse; all backend service credentials and API keys reside in Google Cloud Secret Manager (zero secrets in code or git).
- **Prompt Injection Defense**: Treat all user-supplied text, transcribed audio, and OCR extracted from images as untrusted data. Sanitize and isolate user inputs within strict parameter boundaries before forwarding to LLMs.
- **Input Validation & Rate Limiting**: Validate every request body against Pydantic / Zod schemas; enforce rate limits at the edge / Cloud Armor.

### II. Privacy & PII Minimization
- **PII Masking**: Mask phone numbers, direct contact details, and precise street addresses until a pickup match is confirmed between donor and NGO.
- **LLM Redaction**: Automatically redact phone numbers, emails, and sensitive personal identifiers before passing prompts to Vertex AI / Gemini models.
- **Data Minimization**: Collect only operational data necessary for dispatching and verification.

### III. Reliable AI with Deterministic Safety Gates
- **Structured Outputs**: Every LLM invocation MUST output structured JSON strictly validated by schemas (Pydantic in Python, Zod in TypeScript). Unparsable or schema-violating outputs trigger automatic retries with fallbacks.
- **Deterministic Food-Safety Gate**: An LLM NEVER makes the final food-safety approval in isolation. Deterministic rule checks (safe holding temperature, shelf-life hours, allergens, transit window) take precedence. AI reasoning provides risk explanations, but violations instantly flag `Risky` or `Rejected`.
- **Human-in-the-Loop Override**: Any listing flagged as `Risky` mandates explicit donor/NGO confirmation or administrator review.
- **Resilience**: Enforce explicit timeouts (e.g. 10s max per agent call), exponential backoff retries, and graceful degradation paths.

### IV. Efficiency & High Performance
- **Streaming & Responsiveness**: Stream long-running responses where applicable; achieve end-to-end listing-to-match within 60 seconds.
- **Caching & Token Budgets**: Cache repeated geospatial queries, geocoding lookups, and static safety guidelines. Cap token usage per model call with strict max tokens.
- **Request Profiling**: Measure, log, and monitor latency (P50, P95, P99) and estimated Vertex AI token cost per transaction.

### V. Comprehensive Testing & Evaluation Suite
- **Unit Testing**: Strict unit test coverage for deterministic food-safety rules, matching heuristics, and schema validators.
- **Agent Pipeline Integration Tests**: Automated pipeline tests verifying multi-agent handoffs (Intake -> Safety -> Matching -> Logistics).
- **Evaluation Dataset**: Maintain a curated evaluation dataset of at least 30 diverse sample food listings (spanning valid meals, borderline perishables, expired items, allergen edge cases, and adversarial prompt injections). Validate >= 90% extraction accuracy and 0% false safety approvals.

### VI. Observability & BigQuery Metrics
- **Structured Logging**: Emit structured JSON logs with correlation/trace IDs linking listing creation to final delivery.
- **Impact & Operational Metrics**: Stream lifecycle events to Google BigQuery for near-real-time analytics (kg rescued, meals served, match times, expired-before-pickup rate).

### VII. Google Technology First
- Prioritize Google Cloud and Google developer ecosystems wherever suitable:
  - **Vertex AI / Gemini 2.5 Flash & Pro**: Agent intelligence and multimodal perception.
  - **Firebase Auth, App Check, Firestore, Cloud Storage, Firebase Hosting**: Frontend auth, operational DB, and hosting.
  - **Google Cloud Run**: Serverless container execution for FastAPI agents.
  - **Google Cloud Secret Manager**: Secure credentials management.
  - **Google Maps Platform (JS API / Distance Matrix)**: Geospatial visualization and routing.
  - **Google BigQuery & BigQuery ML**: Data warehousing and surplus hotspot prediction.
- All third-party and open-source packages must be documented in `README.md`.

### VIII. Original Work, Typing & Code Craft
- Write original, production-ready, clean code with strict type annotations (Python type hints, TypeScript strict mode).
- Maintain clear modular separation between UI, agent orchestration, safety rules, and database access.

## Hackathon Judging Alignment

| Judging Dimension | FoodLoop Architectural Guarantee |
| :--- | :--- |
| **Security** | Role-based custom claims, Firestore least-privilege rules, App Check, Secret Manager, prompt-injection guard, PII redaction. |
| **Efficiency** | Cached distance lookups, streaming API responses, token caps, sub-60-second listing-to-match latency. |
| **Technology Implemented** | Multi-agent autonomous workflow (Intake, Safety, Matching, Logistics), deterministic rule engine, PWA, BigQuery pipeline. |
| **Performance** | FastAPI async runtime on Cloud Run, client-side optimistic UI, low-latency Gemini 2.5 Flash intake. |
| **Google Technology Used** | Gemini on Vertex AI, Firebase (Auth, Firestore, Storage, Hosting), Google Cloud Run, Secret Manager, BigQuery, Google Maps. |

## Development Workflow & Quality Gates

1. **Schema-First Specification**: Every feature must define input/output schemas and security boundaries before implementation.
2. **Deterministic Safety Rules**: Any safety rule modification must include unit test cases for safe, risky, and reject scenarios.
3. **Agent Evaluation Gate**: Model prompt changes must run against the 30-sample evaluation suite; regression in safety or extraction accuracy fails the build.
4. **Code Quality**: Zero unhandled TypeScript/Python type errors, zero committed secrets.

## Governance

- The FoodLoop Constitution supersedes ad-hoc coding decisions or agent shortcuts.
- Any architectural amendment requires updating this document with documented rationale and version increment.
- Adherence to security, privacy, and deterministic safety rules is non-negotiable for all PRs and implementations.

**Version**: 1.0.0 | **Ratified**: 2026-10-23 | **Last Amended**: 2026-10-23
