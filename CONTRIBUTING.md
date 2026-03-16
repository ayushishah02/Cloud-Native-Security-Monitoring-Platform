# Cloud-Native Security Monitoring Platform (Docker • Kubernetes • Terraform)

## 📌 Project Overview

This project builds a **small cloud-native security monitoring platform** that observes a web application, collects security-relevant events, and visualizes them in a dashboard — using modern DevSecOps tooling.

The focus is **not** on building a complex application, but on **how the system is packaged, deployed, monitored, secured, and automated** using industry-standard technologies.

**Core technologies used:**
- **Docker** – Package each component into containers  
- **Kubernetes** – Run, scale, and manage the platform reliably  
- **Terraform** – Provision the cloud infrastructure using Infrastructure-as-Code  
---

## 🎯 Project Goal

To design and deploy a **mini security monitoring system** that can:

- Observe application behavior (logins, failures, errors)
- Centralize security-relevant logs
- Visualize activity via dashboards
- Detect suspicious patterns (e.g., brute-force attempts)
- Run in a modern, automated, cloud-ready environment

This project mirrors how **real-world SecOps / DevSecOps teams** build and operate monitoring platforms at a smaller scale.

---

## 🧠 Use Case

Imagine a company with a web application where users log in.

They want to:
- Detect suspicious login behavior  
- Monitor errors that may signal vulnerabilities  
- Centralize logs instead of checking servers manually  
- View security trends visually  
- Trigger alerts when something looks wrong  

This project is a **mini version of a SIEM / security monitoring solution**:

**Collect → Store → Visualize → Alert**

---

## 🏗️ Architecture (High Level)

The platform consists of:

- A **simple web application** that generates security events  
- A **log collection pipeline**  
- A **central log storage/search backend**  
- A **dashboard** for visualization  
- **Containerized services** orchestrated by Kubernetes  
- **Cloud infrastructure** provisioned via Terraform  

---

## 🛠️ Project Phases & Timeline

This repository tracks progress through each phase.

---

### 🔹 Phase 0 — Security-Flavored Application

**What is built:**
- A simple web app (e.g., login page + API)
- Logs:
  - Successful logins
  - Failed logins
  - Repeated attempts (simulated suspicious behavior)

**Why it matters:**
- Generates realistic security events
- Simulates a real company web portal
- Provides data to monitor and detect threats

**Status:** ✔️ Completed 

---

### 🔹 Phase 1 — Docker: Containerizing the Platform

**What is containerized:**
- Web application
- Log collector/shipper
- Log storage/search backend
- Visualization/dashboard service

**Key ideas:**
- Each component runs in its own container
- Containers bundle code + dependencies
- Portable, repeatable deployments

**What this demonstrates:**
- Component-based architecture
- Real-world containerization practices

**Status:** ✔️ Completed 

---

### 🔹 Phase 2 — Kubernetes: Running It Like Production

**What Kubernetes handles:**
- Deploying and managing containers
- Restarting failed services
- Scaling components
- Service-to-service communication
- Traffic routing

**Security-focused concepts introduced:**
- Separating public vs internal services
- Using Kubernetes Secrets for sensitive values
- Basic network isolation between components

**What this demonstrates:**
- Operating a multi-service platform
- Production-style deployment patterns
- Foundational Kubernetes security awareness

**Status:** ✔️ Completed

---

### 🔹 Phase 3 — Terraform: Infrastructure-as-Code

**What Terraform provisions:**
- Cloud virtual network
- Kubernetes cluster
- Storage for logs
- Access and security rules

**Key ideas:**
- No manual cloud console setup
- Entire environment defined as code
- Easy to recreate, audit, and version

**Why this matters:**
- Critical for security, compliance, and scalability
- Industry standard for cloud infrastructure

**What this demonstrates:**
- Infrastructure-as-Code skills
- Cloud-native security mindset

**Status:** ✔️ Completed

---

### 🔹 Phase 4 — Security & Observability (SecOps Focus)

**Security capabilities added:**
- Centralized log ingestion
- Dashboards showing:
  - Failed login attempts
  - Top offending IPs
  - Error spikes
- Alerting rules (example):
  - Too many failed logins from one IP in X minutes

**Optional enhancements:**
- Container image vulnerability scanning
- TLS/HTTPS for services
- Role-based access control
- Least-privilege access patterns

**What this demonstrates:**
- Security operations thinking
- Detection & monitoring fundamentals
- Cloud-native observability skills

**Status:** ✔️ Completed

---

## 📊 Progress Tracking

| Phase | Description | Status |
|------|------------|--------|
| Phase 0 | Security app | ✔️ |
| Phase 1 | Docker containerization | ✔️ |
| Phase 2 | Kubernetes deployment | ✔️ |
| Phase 3 | Terraform infrastructure | ✔️ |
| Phase 4 | Security & observability | ✔️ |

---

## 🎓 Skills Demonstrated

- Docker & containerization
- Kubernetes orchestration
- Terraform & Infrastructure-as-Code
- Cloud-native security concepts
- Log aggregation & monitoring
- Security event detection
- DevSecOps mindset

---

## 🚀 Why This Project Matters

This repository demonstrates **how modern security platforms are built and operated**, not just how applications are coded.

It shows:
- Real-world tooling
- Production-style architecture
- Security thinking embedded from the start
- Clear progression from local development → cloud deployment

---

## 📌 Status

🟡 **Project in progress**  
This README will be updated as each phase is completed.

---

