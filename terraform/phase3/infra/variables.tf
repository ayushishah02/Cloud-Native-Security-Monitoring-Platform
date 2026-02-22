variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "cnsm-phase3"
}

variable "allowed_ssh_cidr" {
  description = "Your public IP in CIDR format (example: 1.2.3.4/32)"
  type        = string
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type for the K3s node"
  default     = "t3.small"
}

variable "public_key_path" {
  description = "Path to your SSH public key (example: C:\\Users\\ayush\\.ssh\\id_ed25519.pub)"
  type        = string
}

variable "nodeport_port" {
  description = "NodePort your app will expose"
  type        = number
  default     = 30080
}
