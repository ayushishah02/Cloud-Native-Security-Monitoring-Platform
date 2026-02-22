# 🚀 Phase 3 – Infrastructure as Code (AWS + Terraform + K3s + ECR)

## 📌 Overview

In Phase 3, the Cloud-Native Security Monitoring Platform was migrated from a local Kubernetes environment to a fully provisioned AWS infrastructure using **Terraform**.

This phase introduces:

- Infrastructure as Code (IaC)
- Automated EC2 provisioning
- K3s Kubernetes bootstrap via `user_data`
- IAM-based authentication for Amazon ECR
- Secure container image pulling without static credentials
- Public application exposure via Kubernetes NodePort

The result is a reproducible, production-style cloud deployment.

---

## 🏗 Architecture

### Infrastructure Provisioned via Terraform

- VPC (`10.20.0.0/16`)
- Public Subnet
- Internet Gateway
- Route Table + Association
- Security Group (SSH restricted to developer IP)
- EC2 Instance (Ubuntu 22.04)
- IAM Role (ECR ReadOnly)
- IAM Instance Profile attached to EC2
- SSH Key Pair

### Bootstrapped Automatically on EC2

- K3s Kubernetes
- Containerd runtime
- Systemd-managed control plane

### Application Flow

Browser → EC2 Public IP → NodePort (30080) → Kubernetes Service → Frontend Pods → ECR Image

---

## 🔐 Security Design

Phase 3 intentionally avoids static credentials.

### IAM Best Practice Implementation

- EC2 instance assumes IAM role:
  `AmazonEC2ContainerRegistryReadOnly`
- No AWS access keys stored on the server
- Kubernetes pulls images from ECR using instance metadata credentials
- SSH access restricted to `/32` CIDR
- No hardcoded secrets inside Terraform

This mirrors real-world cloud security practices.

---

## 📦 ECR Integration

Frontend image stored in Amazon ECR:

`280934867410.dkr.ecr.us-east-1.amazonaws.com/secureworks-frontend:phase3`

Deployment image reference:

```yaml
image: 280934867410.dkr.ecr.us-east-1.amazonaws.com/secureworks-frontend:phase3
