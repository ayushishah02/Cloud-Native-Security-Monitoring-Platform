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

---
## ⚙️ Deployment Steps

### 1️⃣ Provision Infrastructure

From:

`terraform/phase3/infra`

Run:

```bash
terraform init

terraform plan \
  -var="allowed_ssh_cidr=<YOUR_PUBLIC_IP>/32" \
  -var="public_key_path=C:/Users/<user>/.ssh/id_ed25519_phase3.pub"

terraform apply
```

Outputs:

- `ec2_public_ip`
- `ssh_hint`

---

### 2️⃣ Verify K3s

SSH into the instance:

```bash
ssh -i <private_key> ubuntu@<EC2_PUBLIC_IP>
```

Check cluster:

```bash
sudo k3s kubectl get nodes
sudo k3s kubectl get pods -A
```

---

### 3️⃣ Deploy Application

Copy manifests:

```bash
scp -i <private_key> -r k8s ubuntu@<EC2_PUBLIC_IP>:~/cnsm/
```

Apply:

```bash
cd ~/cnsm/k8s

sudo k3s kubectl apply -f namespace.yaml
sudo k3s kubectl apply -f frontend-deployment.yaml
sudo k3s kubectl apply -f frontend-service.yaml
```

Verify:

```bash
sudo k3s kubectl -n secureworks get deploy,svc,pods
```

---

## 🌐 Access the Application

Open in browser:

`http://<EC2_PUBLIC_IP>:30080`

Health check:

```bash
curl -I http://<EC2_PUBLIC_IP>:30080
```

Expected response:

```
HTTP/1.1 200 OK
```

