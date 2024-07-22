output "bestion_host_ip" {
  description = "Public IP address of the public instance"
  value       = module.instances.bestion_host_ip
}

output "django_instance_ip" {
  description = "Public IP address of the public instance"
  value       = module.instances.django_instance_ip
}
output "rds_endpoint" {
  value = module.rds.db_instance_endpoint
}
