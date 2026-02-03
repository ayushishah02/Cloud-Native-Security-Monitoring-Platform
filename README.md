# Phase 2 — Kubernetes Deployment (Completed)

## Overview
In Phase 2, the SecureWorks frontend application was deployed onto a local Kubernetes cluster using Docker Desktop.

This phase focused on running the previously containerized application in a **production-style Kubernetes environment**, validating pod lifecycle management, service exposure, and internal Kubernetes networking.

The emphasis was on **deployment correctness and Kubernetes fundamentals**, not observability or security tooling yet.

---

## Phase 2 Objectives
The goals of this phase were to:

- Deploy the Dockerized frontend using Kubernetes manifests
- Manage the application using a Kubernetes Deployment
- Run multiple replicas for availability
- Expose the application externally using a Service
- Validate service-to-pod routing using selectors and endpoints
- Debug and resolve real-world Kubernetes configuration issues

---

## What Was Implemented

### Kubernetes Deployment
- Created a `Deployment` for the frontend application
- Configured replica count for high availability
- Enabled rolling updates for safe changes
- Defined CPU and memory requests/limits
- Added readiness and liveness HTTP probes
- Verified automatic pod restarts on failure

### Kubernetes Service
- Created a `NodePort` Service for external access
- Correctly mapped Service port `80` → container port `8080`
- Used label selectors to route traffic to Pods
- Validated dynamic endpoint population

### Networking & Validation
- Verified Pod scheduling and node placement
- Confirmed Pods received cluster IPs
- Validated Service endpoints matched running Pods
- Confirmed external access via `http://localhost:30080`

---

## Files Added / Modified in This Phase

k8s/frontend-deployment.yaml
k8s/frontend-service.yaml
app/frontend/Dockerfile
app/frontend/nginx.conf


These changes ensured the container image and Kubernetes configuration were fully aligned.

---

## Validation & Verification
Deployment correctness was verified using Kubernetes-native inspection commands:

- `kubectl get deploy`
- `kubectl get pods -o wide`
- `kubectl get svc`
- `kubectl get endpoints`
- `kubectl describe deploy`

Successful validation showed:
- Pods in `Running` state (`READY 1/1`)
- Deployment available with desired replicas
- Service correctly routing traffic to Pods
- Application accessible externally

---

## Outcome
At the end of Phase 2, the SecureWorks frontend application is:

- Running as replicated Pods in Kubernetes
- Managed by a Deployment with rolling updates
- Exposed externally via a NodePort Service
- Correctly wired through Kubernetes networking
- Ready for infrastructure automation and security tooling

**Phase 2 Status:** ✅ Completed
