# SRE.Space Insure – AIOps SRE Control Plane Demo

**SRE.Space Insure** is a modern, reliable insurance platform demo designed to showcase **Advanced Observability**, **OpenTelemetry**, and **AIOps workflows**.

![Status](https://img.shields.io/badge/Status-Active-success)
![Telemetry](https://img.shields.io/badge/Telemetry-OpenTelemetry-blue)
![Backend](https://img.shields.io/badge/Backend-New%20Relic-008c99)

## 🚀 Features

*   **Microservices Architecture**:
    *   **Frontend**: Nginx-hosted UI with Glassmorphism design.
    *   **Backend**: FastAPI Python service with full logic.
*   **Full Observability Stack**:
    *   **Traces**: Named spans for Critical User Journeys (CUJ) like *Login*, *File Claim*, *Pay Premium*.
    *   **Metrics**: Custom counters (e.g., `login_requests_total`).
    *   **Logs**: Structured application logs via OTLP.
*   **AIOps Ready**:
    *   Data flows via **OpenTelemetry Collector** directly to **New Relic**.
    *   Kubernetes-ready manifests with metadata tagging.

---

## 🏗️ Directory Structure

```bash
aiops-sre-control-plane/
├── apps/
│   ├── demo-insurance/
│   │   ├── backend/       # FastAPI App + OTel Instrumentation
│   │   └── frontend/      # HTML/JS/CSS UI
├── k8s/                   # Kubernetes Manifests (Deployment, Secrets, Collector)
├── telemetry/
│   └── opentelemetry/     # OTel Collector Config
├── docker-compose.yml     # Local Dev Stack
└── .env                   # Secrets (GitIgnored)
```

---

## ⚡ Getting Started

### Prerequisites
*   Docker Desktop
*   New Relic Account (License Key)

### 1. Setup Secrets
Create a `.env` file in the root directory:
```bash
NEW_RELIC_LICENSE_KEY=your_40_char_license_key
```

### 2. Run Locally (Docker Compose)
Spin up the entire stack with a single command:
```bash
docker compose up -d --build
```
*   **Frontend**: [http://localhost:3000](http://localhost:3000)
*   **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **OTel Collector logs**: `docker compose logs -f otel-collector`

### 3. Deploy to Kubernetes
Deploy to any K8s cluster (Minikube, Kind, EKS, GKE).

**First, update secrets**:
Edit `k8s/secrets.yaml` with your actual New Relic license key.

**Then apply manifests**:
```bash
# Build local images (if using Minikube/Docker Desktop)
docker build -t insurance-backend:latest ./apps/demo-insurance/backend
docker build -t insurance-frontend:latest ./apps/demo-insurance/frontend

# Deploy
kubectl apply -f k8s/
```
*   **Frontend Access**: [http://localhost:30000](http://localhost:30000) (NodePort)

---

## 📊 Observability (New Relic)

Once running, generate traffic using the UI or `curl`. Go to **[one.newrelic.com](https://one.newrelic.com)** to visualize:

1.  **APM**: Search for `insurance-backend` to see throughput and errors.
2.  **Distributed Tracing**: View waterfalls for `CUJ-Login` or `CUJ-File-Claim`.
3.  **Kubernetes**: If deployed to K8s, filter data by `k8s.pod.name` or `k8s.namespace.name`.

---

## 🛠️ Critical User Journeys (CUJs)

| Journey | Span Name | Description |
| :--- | :--- | :--- |
| **Login** | `CUJ-Login` | User authentication flow. |
| **View Policy** | `CUJ-View-Policy` | Retrieving active policy details. |
| **File Claim** | `CUJ-File-Claim` | Submission of a new insurance claim. |
| **Pay Premium** | `CUJ-Premium-Payment` | Payment processing transaction. |

---

