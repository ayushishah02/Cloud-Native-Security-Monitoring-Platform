# Phase 1 — Dockerization (Completed)

## Overview

In Phase 1, the SecureWorks frontend application created in Phase 0 was
successfully containerized using Docker.

The goal of this phase was to package the application into a **portable,
production-style container image** that can run consistently across environments,
independent of local tooling.

This phase establishes the foundation for Kubernetes deployment in Phase 2.

---

## What Was Accomplished

- Containerized the SecureWorks frontend application
- Used a **multi-stage Docker build** for efficiency and security
- Built the frontend using Node.js inside Docker
- Served the production build using **Nginx**
- Verified the containerized application runs locally
- Ensured clean repository hygiene (`.dockerignore`, no node_modules committed)

---

## Docker Design Choices

### Multi-Stage Build

The Dockerfile uses two stages:

1. **Build Stage (Node.js)**
   - Installs dependencies
   - Builds the frontend into static assets

2. **Runtime Stage (Nginx)**
   - Serves only the built static files
   - No Node.js runtime included
   - Smaller, more secure production image

This mirrors real-world frontend deployment patterns.

---

## Files Added in This Phase
 app/frontend/
- Dockerfile
- .dockerignore
- nginx.conf