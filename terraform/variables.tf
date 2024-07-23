# region & available_zone
variable "region" {
  description = "AWS region"
  type        = string
}
variable "availability_zoneA" {
  description = "The availability zone for the first public subnet"
  type        = string
}
variable "availability_zoneB" {
  description = "The availability zone for the second public subnet"
  type        = string
}

# CIDR
variable "public_cidr" {
  description = "CIDR block for public"
  type        = string
}
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}
variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
}
variable "private_subnet_1_cidr" {
  description = "CIDR block for the first private subnet"
  type        = string
}
variable "private_subnet_2_cidr" {
  description = "CIDR block for the second private subnet"
  type        = string
}

# RDS
variable "db_username" {
  description = "The username for the RDS instance"
  type        = string
}
variable "db_password" {
  description = "The password for the RDS instance"
  type        = string
  sensitive   = true
}

# allowed_ips
variable "allowed_ips" {
  description = "List of IPs allowed to access port 9200"
  type = list(string)
}

