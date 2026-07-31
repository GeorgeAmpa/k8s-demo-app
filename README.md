# Kubernetes Demo App

![CI/CD](https://github.com/GeorgeAmpa/k8s-demo-app/actions/workflows/ci-cd.yml/badge.svg)

A containerized Python Flask web application deployed on Kubernetes, demonstrating core DevOps practices including Docker containerization, Kubernetes orchestration, self-healing, and zero-downtime rolling updates — with a full CI/CD pipeline via GitHub Actions.

## CI/CD Pipeline

```
git push → GitHub Actions → docker build → push to ghcr.io → ready to deploy
```

Every push to `main` automatically:
1. Builds a new Docker image
2. Tags it with the git commit SHA
3. Pushes it to GitHub Container Registry (ghcr.io)

## Architecture

```
Browser → Kubernetes Service (NodePort) → Kubernetes Deployment → Flask App (Pod x2)
```

## Project Structure

```
k8s-demo-app/
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions CI/CD pipeline
├── app/
│   ├── app.py              # Flask web application
│   └── requirements.txt    # Python dependencies
├── k8s/
│   ├── deployment.yaml     # Kubernetes Deployment (2 replicas)
│   ├── service.yaml        # Kubernetes Service (NodePort)
│   └── servicemonitor.yaml # Prometheus ServiceMonitor
├── Dockerfile              # Container image definition
└── README.md
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Containerization | Dockerfile with optimized layer caching |
| High Availability | 2 replicas running simultaneously |
| Self-healing | Kubernetes auto-restarts crashed pods |
| Zero-downtime deploy | Rolling update strategy |
| Health checks | Liveness & Readiness probes on `/health` |
| Resource management | CPU and memory requests/limits defined |
| Configuration | Environment variables injected via Deployment |
| Observability | Prometheus metrics + Grafana dashboards |
| Custom metrics | HTTP request count and latency per endpoint |

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Getting Started

**1. Start the local Kubernetes cluster:**
```bash
minikube start --driver=docker
```

**2. Point Docker to minikube's daemon:**
```bash
minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

**3. Build the Docker image:**
```bash
docker build -t k8s-demo-app:1.0.0 .
```

**4. Deploy to Kubernetes:**
```bash
kubectl apply -f k8s/
```

**5. Open in browser:**
```bash
minikube service k8s-demo-app
```

## Useful Commands

```bash
# Check running pods
kubectl get pods

# Check service
kubectl get services

# View pod logs
kubectl logs -l app=k8s-demo-app

# Deploy a new version
docker build -t k8s-demo-app:2.0.0 .
kubectl set image deployment/k8s-demo-app k8s-demo-app=k8s-demo-app:2.0.0

# Watch rolling update
kubectl rollout status deployment/k8s-demo-app

# Rollback to previous version
kubectl rollout undo deployment/k8s-demo-app

# Scale up/down
kubectl scale deployment/k8s-demo-app --replicas=3
```

## Monitoring Stack

Deployed via Helm using `kube-prometheus-stack`:

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

Custom Flask metrics exposed at `/metrics`:
- `http_requests_total` — request count by endpoint, method, status
- `http_request_duration_seconds` — request latency histogram

Access Grafana dashboard:
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

## Tech Stack

- **Application:** Python 3.12 / Flask
- **Containerization:** Docker
- **Orchestration:** Kubernetes (minikube)
- **CI/CD:** GitHub Actions
- **Container Registry:** GitHub Container Registry (ghcr.io)
- **Monitoring:** Prometheus + Grafana (via Helm)
- **OS:** Linux (python:3.12-slim base image)
