# FoodLoop Quickstart Guide

This guide covers bootstrapping the FoodLoop project locally for development, testing, and evaluation.

## Prerequisites
- Node.js 20+ & npm / pnpm
- Python 3.11+ / uv (`uv run ...`)
- Firebase CLI (`npm install -g firebase-tools`)
- Google Cloud SDK (`gcloud`) with Vertex AI API enabled

## Setup Steps

### 1. Backend (FastAPI & Agent Service)
```bash
cd backend
uv sync
# Copy environment template
cp .env.example .env
# Start local API server
uv run uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (Next.js PWA)
```bash
cd frontend
npm install
npm run dev
# App starts at http://localhost:3000
```

### 3. Firebase Emulator (Optional for local Firestore & Auth)
```bash
firebase emulators:start --only auth,firestore,storage
```

### 4. Running the Agent Evaluation Benchmark Suite
```bash
cd backend
# Runs the 30-sample evaluation dataset against the Intake & Safety agents
uv run pytest tests/test_evaluation_suite.py -v
```

### 5. Running Seed Data
```bash
cd backend
# Seeds 5 NGOs, 3 Volunteers, 10 Donors, and initial historical records
uv run python -m app.scripts.seed_demo_data
```
