output "ec2_public_ip" {
  value = aws_instance.k3s.public_ip
}

output "ssh_hint" {
  value = "ssh -i <YOUR_PRIVATE_KEY_PATH> ubuntu@${aws_instance.k3s.public_ip}"
}

############################################################
# New outputs for IAM Role + Instance Profile
############################################################

output "ec2_instance_profile_name" {
  value = aws_iam_instance_profile.ec2_profile.name
}

output "ec2_role_name" {
  value = aws_iam_role.ec2_ecr_readonly.name
}