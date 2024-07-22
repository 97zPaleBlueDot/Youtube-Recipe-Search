output "bestion_host_ip" {
  description = "Public IP address of the public instance"
  value       = aws_instance.bastion_host.public_ip
}

output "django_instance_ip" {
  description = "Public IP address of the public instance"
  value       = aws_instance.django_instance.public_ip
}

# output "private_instance_ip" {
#   description = "Private IP address of the private instance"
#   value       = aws_instance.private_instance.private_ip
# }