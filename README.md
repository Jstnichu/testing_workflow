# Sample CI/CD + Kubernetes demo

This repository is a minimal sample to learn CI and CD with GitHub Actions and Kubernetes.

What is included
- A tiny Node.js Express app (`index.js`) and `package.json`.
- `Dockerfile` and `.dockerignore` to build a container image.
- Kubernetes manifests in `k8s/` (`deployment.yaml`, `service.yaml`).
- GitHub Actions workflows:
  - `.github/workflows/ci.yml` — build and push Docker image to Docker Hub.
  - `.github/workflows/cd.yml` — deploy image to Kubernetes using a kubeconfig secret.

Required secrets (configure in your GitHub repo settings > Secrets):
- `ACR_USERNAME` — ACR username (service principal appId or admin user).
- `ACR_PASSWORD` — ACR password (service principal password or admin user password).
- `KUBE_CONFIG` — base64 encoded kubeconfig file for your cluster (run `cat ~/.kube/config | base64`).

Quick local steps
1. Build and run locally:
   npm install
   npm start
   Visit http://localhost:8080

2. Build container locally:
   docker build -t username/sample-app:local .
   docker run -p 8080:8080 username/sample-app:local

3. Test on a local Kubernetes cluster (minikube/kind):
   - For minikube: run `minikube start` then `kubectl apply -f k8s/`.
   - For kind: `kind create cluster` then `kubectl apply -f k8s/`.

How CI/CD works in this demo
- CI (`ci.yml`) runs on push to `main`: installs dependencies, runs tests, logs into Azure Container Registry (`3aidfacr20082025161558dev.azurecr.io`) and pushes two tags (latest and commit sha).
- CD (`cd.yml`) runs on push to `main` (or manual dispatch): decodes `KUBE_CONFIG` secret, and updates the Deployment image or applies the manifests if missing.

Notes and next steps
- This is a minimal example intended for learning. Real projects often require:
  - Image signing/scan, more robust tagging (semver), or image promotion pipelines.
  - Secrets management (Kubernetes Secrets, external secret stores), role-restricted service accounts for CI runners.
  - Health/readiness probes and resource requests/limits in k8s manifests.

If you want, I can:
- Switch the example to use GitHub Container Registry (GHCR) instead of Docker Hub.
- Add a simple test and a GitHub Actions matrix to validate multiple Node versions.
- Add health/readiness probes and a HorizontalPodAutoscaler manifest.
