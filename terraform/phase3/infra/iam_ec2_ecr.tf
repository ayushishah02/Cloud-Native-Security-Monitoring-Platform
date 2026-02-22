data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# 2) IAM Role: the identity EC2 will assume.
resource "aws_iam_role" "ec2_ecr_readonly" {
  name               = "${var.project_name}-ec2-ecr-readonly"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json

  tags = {
    Name = "${var.project_name}-ec2-ecr-readonly"
  }
}

# 3) Attach AWS-managed ECR read-only policy to the role.
# This policy includes permissions needed to pull images.
resource "aws_iam_role_policy_attachment" "ecr_readonly_attach" {
  role       = aws_iam_role.ec2_ecr_readonly.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# 4) Instance Profile: EC2 can't attach a role directly.
# EC2 attaches an Instance Profile, which contains the role.
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2_ecr_readonly.name
}