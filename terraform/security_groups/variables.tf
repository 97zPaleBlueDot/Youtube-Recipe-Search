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