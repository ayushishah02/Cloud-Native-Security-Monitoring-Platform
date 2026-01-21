# SecureWorks Demo App — Phase 0  
### Security-Flavored Application (Telemetry Source)

## Overview
**SecureWorks Demo App** is a simulated internal company login portal designed to generate **realistic, structured security events** for monitoring and detection.

This branch represents **Phase 0** of a larger **Cloud-Native Security Monitoring Platform** project that will progressively incorporate Docker, Kubernetes, Terraform, and SecOps observability tooling.

> **Phase 0 focus:**  
> Creating a reliable source of authentication and authorization security telemetry — not building a complex business application.

---

## Phase 0 Objectives
The goals of this phase are to:

- Simulate enterprise-style authentication behavior
- Generate structured, machine-readable security logs
- Detect suspicious patterns such as brute-force login attempts
- Define a consistent log schema used across all future phases
- Prepare the application for containerization and orchestration

---

## Application Features

### Authentication Portal (`/login`)
- Clean, professional login interface
- Email and password fields with loading state
- Generic error message on failure:  
  **“Invalid email or password”**
- Prevents user enumeration by design
- Redirects to dashboard on successful login

---

### User Dashboard (`/dashboard`)
Protected route — authentication required.

Displays:
- Welcome message with user email
- User role (`user` or `admin`)
- Last login timestamp
- Logout button (JWT cleared client-side)

Admin users see a link to the Security Audit Panel.

---

### Admin Panel (`/admin`)
Protected route — **admin role required**.

- “Security Audit Panel” view
- Placeholder table demonstrating log format:
  - timestamp
  - event_type
  - username
  - ip_address
  - result
- Unauthorized access attempts are denied and logged

---

## Demo Users (Phase 0 Only)
Authentication uses **hardcoded demo users** for simplicity.

| Email | Password | Role |
|-----|---------|------|
| user@secureworks.demo | Password123! | user |
| admin@secureworks.demo | AdminPassword123! | admin |

> No database is used for user storage in Phase 0.

---

## API Endpoints

| Endpoint | Description |
|-------|------------|
| POST `/api/auth/login` | Authenticate user and issue JWT |
| POST `/api/auth/logout` | Log logout event (client clears JWT) |
| GET `/api/auth/me` | Validate JWT and return user info |

Authentication is implemented using **JWTs** for stateless session handling.

---

## Structured Security Logging

All authentication and authorization events are logged **server-side** from Supabase Edge Functions as **structured JSON**.

### Logged Events

| Event Type | Description |
|----------|------------|
| `auth.login.success` | Successful login |
| `auth.login.failure` | Failed login |
| `auth.login.suspicious` | Brute-force threshold exceeded |
| `auth.login.blocked` | Login blocked due to repeated failures |
| `authz.access.denied` | Unauthorized admin access attempt |
| `auth.logout.success` | User logout |

---

### Log Schema
Each event is emitted as a **single JSON object**:

```json
{
  "timestamp": "2026-01-21T10:30:00.000Z",
  "event_type": "auth.login.failure",
  "username": "attacker@example.com",
  "ip_address": "203.0.113.50",
  "user_agent": "Mozilla/5.0...",
  "result": "failure",
  "reason": "invalid_password",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}

