# Tasks: FoodLoop Surplus Food Rescue Multi-Agent Platform

**Input**: Design documents from `/specs/001-foodloop-core/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/api.yaml`)

**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/api.yaml`

**Organization**: Structured into 7 phases aligned with the implementation roadmap.

## Format: `[ID] [P?] [Phase/Story] Description`
- **[P]**: Parallelizable task
- Includes explicit target file paths

---

## Phase 1: Setup & Foundations (Auth, Roles, Firestore Rules)

**Goal**: Establish project directory structure, dependencies, Firebase Auth role verification, custom claims, and Firestore security rules.

- [x] T001 [Setup] Initialize backend directory structure, FastAPI app, and requirements in `backend/`
- [x] T002 [Setup] Initialize frontend Next.js 15 PWA scaffolding with Tailwind CSS in `frontend/`
- [x] T003 [P] [Auth] Implement Firebase Auth token verification middleware and custom claims validation (`donor`, `ngo`, `volunteer`, `admin`) in `backend/app/api/auth.py`
- [x] T004 [P] [Security] Implement Firestore Security Rules enforcing role-based least privilege and PII subcollection isolation in `firestore.rules`
- [x] T005 [Security] Implement Secret Manager configuration and App Check validation in `backend/app/core/security.py`

**Checkpoint**: Foundation ready. Auth, role claims, and security rules verified.

---

## Phase 2: Intake Agent with Schema-Validated Output (User Story 1 - P1)

**Goal**: Multimodal extraction from food photo or voice note via Gemini 2.5 Flash with Pydantic JSON schema validation and prompt injection defenses.

- [x] T006 [P] [Intake] Define Pydantic models for `FoodIntakeDraft` and `FoodListing` in `backend/app/schemas/foodloop.py`
- [x] T007 [P] [Security] Implement multimodal prompt injection defense layer and PII scrubbing in `backend/app/core/guardrails.py`
- [x] T008 [Intake] Implement `IntakeAgent` using Gemini 2.5 Flash on Vertex AI in `backend/app/agents/intake_agent.py`
- [x] T009 [Intake] Implement FastAPI intake endpoint `POST /agent/intake` supporting image/audio uploads in `backend/app/api/intake.py`
- [x] T010 [P] [Tests] Unit test `IntakeAgent` schema parsing, retries, and prompt-injection guard in `backend/tests/test_intake_schemas.py`

**Checkpoint**: Donors can upload image/audio and receive validated structured food listings.

---

## Phase 3: Deterministic Food-Safety Rules Engine (User Story 2 - P1)

**Goal**: Deterministic FSSAI rule engine with AI reasoning generating `Safe`, `Risky`, or `Rejected` verdicts with natural language explanations.

- [x] T011 [Safety] Implement deterministic FSSAI food-safety rule engine (ambient temperature thresholds, shelf life, high-risk ingredients) in `backend/app/rules/fssai_rules.py`
- [x] T012 [Safety] Implement `SafetyAgent` combining deterministic rule execution with Gemini reasoning in `backend/app/agents/safety_agent.py`
- [x] T013 [Safety] Implement safety endpoint `POST /agent/safety-check` in `backend/app/api/safety.py`
- [x] T014 [P] [Tests] Unit tests for FSSAI safety rules engine across safe, risky, and reject scenarios in `backend/tests/test_safety_rules.py`

**Checkpoint**: Food safety gate fully enforces deterministic limits with 0% auto-approvals for unsafe listings.

---

## Phase 4: Proximity & Urgency Matching Agent (User Story 3 - P1)

**Goal**: Score and rank nearby NGOs within 5 km by distance, capacity deficit, dietary compatibility, and urgency with Gemini-generated rationales.

- [x] T015 [Matching] Implement multi-criteria NGO ranking algorithm in `backend/app/rules/matching_rules.py`
- [x] T016 [Matching] Implement `MatchingAgent` with distance caching and LLM rationale generation in `backend/app/agents/matching_agent.py`
- [x] T017 [Matching] Implement matching endpoint `POST /agent/match` in `backend/app/api/matching.py`
- [x] T018 [P] [Tests] Unit test matching ranking algorithm and distance thresholds in `backend/tests/test_matching_agent.py`

**Checkpoint**: Safe listings are matched to top-ranked NGOs with plain-language explanations in <60 seconds.

---

## Phase 5: Logistics Agent & Real-Time Alerts (User Story 4 & 5 - P2)

**Goal**: NGO match acceptance/decline flow, volunteer dispatch assignment, route calculation, and photo Proof of Delivery (PoD).

- [x] T019 [Logistics] Implement volunteer proximity selector and Google Maps route calculation in `backend/app/agents/logistics_agent.py`
- [x] T020 [Logistics] Implement dispatch endpoint `POST /agent/dispatch` and status update endpoints in `backend/app/api/logistics.py`
- [x] T021 [Volunteer] Implement volunteer task tracking and photo Proof of Delivery upload in `backend/app/api/logistics.py`

**Checkpoint**: Full NGO acceptance, volunteer dispatch, turn-by-turn navigation, and proof-of-delivery loop functional.

---

## Phase 6: BigQuery Pipeline & Impact Analytics Dashboard (User Story 6 - P3)

**Goal**: Stream lifecycle events to BigQuery, calculate social/environmental KPIs, and forecast surplus hotspots.

- [x] T022 [Analytics] Implement BigQuery event streaming client in `backend/app/services/bigquery.py`
- [x] T023 [Analytics] Implement analytics endpoints `GET /analytics/impact` and `GET /analytics/forecast` in `backend/app/api/analytics.py`
- [x] T024 [P] [Frontend] Build Impact & Admin Dashboard with surplus hotspots and KPI cards in `frontend/src/components/ImpactDashboard.tsx`

**Checkpoint**: End-to-end observability, real-time KPI metrics, and ML surplus hotspot cards active.

---

## Phase 7: Evaluation Suite & Demo Seed Data

**Goal**: Comprehensive evaluation benchmark of 30 sample listings and pre-seeded realistic data.

- [x] T025 [Data] Create 30-sample diverse food evaluation dataset (`eval_listings.json`) in `backend/tests/data/`
- [x] T026 [Tests] Implement automated benchmark test suite measuring extraction accuracy (>=90%) and safety precision (100%) in `backend/tests/test_evaluation_suite.py`
- [x] T027 [Demo] Create demo database seeder (5 NGOs, 3 Volunteers, 10 Donors) in `backend/app/scripts/seed_demo_data.py`
- [x] T028 [Docs] Generate project `README.md` disclosing all open-source libraries, APIs, and Google technologies used

**Checkpoint**: All 7 phases implemented, verified by tests, and ready for hackathon presentation.
