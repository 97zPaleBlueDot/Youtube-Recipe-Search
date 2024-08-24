variable "vpc_id" {
  description = "The VPC ID where the security groups will be created"
  type        = string
}

variable "public_cidr" {
  description = "CIDR block for public"
  type        = string
}
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}
variable "allowed_ips" {
  description = "List of IPs allowed to access port 9200"
  type = list(string)
}