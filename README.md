# Phase 1 — Dockerization

## Objective

The goal of Phase 1 is to containerize the SecureWorks frontend application
built in Phase 0 using Docker.

This phase focuses on packaging the application into a portable,
reproducible container image that can run consistently across environments.

---

## What This Phase Covers

- Scaffolding a runnable React frontend (Vite + TypeScript)
- Integrating the SecureWorks UI
- Creating a production-ready Dockerfile
- Building and running the application as a container locally
- Applying Docker best practices (small images, clear entrypoints)

---

## What This Phase Does NOT Cover

- Kubernetes deployments
- Cloud infrastructure
- Centralized logging pipelines
- Alerting or dashboards

These are intentionally handled in later phases.

---

## Deliverables

- Runnable frontend application
- Dockerfile for the frontend
- Docker build and run instructions
- Containerized application accessible via browser

---

## Success Criteria

- `docker build` completes successfully
- `docker run` launches the application
- SecureWorks UI is accessible from the container

---

## Next Phase

Phase 2 — Kubernetes Deployment
