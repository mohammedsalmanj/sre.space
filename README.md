# Phase 1 – Insurance Demo App (Docker Only)

This is Phase 1 of the AIOps SRE Control Plane.

## What is included
- Insurance demo backend (FastAPI)
- Critical User Journeys:
  - Login
  - View Policy
  - File Claim
  - Payment
- Fully containerized using Docker Desktop
- No local Python dependencies required

## How to run
docker compose up --build

## Endpoints
- GET /
- POST /login
- GET /policy/{id}
- POST /claim
- POST /payment
