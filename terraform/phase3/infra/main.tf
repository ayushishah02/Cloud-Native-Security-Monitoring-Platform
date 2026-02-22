############################
# Data Sources
############################

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

############################
# Networking (VPC)
############################

resource "aws_vpc" "main" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.20.1.0/24"
  map_public_ip_on_launch = true

  # safer than "${var.aws_region}a" (some accounts/regions don’t have "a")
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

############################
# Security Group
############################

resource "aws_security_group" "k3s" {
  name        = "${var.project_name}-sg"
  description = "Minimal SG for K3s single node"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH (locked to your IP)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  ingress {
    description = "App NodePort"
    from_port   = var.nodeport_port
    to_port     = var.nodeport_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

############################
# SSH Key Pair
############################

resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key-phase3"
  public_key = file(var.public_key_path)
}

############################
# Compute (EC2 + K3s bootstrap)
############################

resource "aws_instance" "k3s" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.k3s.id]
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = true

  # ✅ Correct reference name
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = file("${path.module}/user_data_k3s.sh")

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
  }

  tags = {
    Name = "${var.project_name}-k3s"
  }
}