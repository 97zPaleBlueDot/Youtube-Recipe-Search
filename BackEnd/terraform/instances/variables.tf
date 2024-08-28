variable "public_subnet_id" {
  description = "The public subnet ID where the Bastion Host will be created"
  type        = string
}

variable "private_subnet_id" {
  description = "The private subnet ID where the Django server will be created"
  type        = string
}

variable "public_sg_id" {
  description = "The security group ID for the public subnet"
  type        = string
}

variable "private_sg_id" {
  description = "The security group ID for the private subnet"
  type        = string
}
variable "django_sg_id" {
  description = "The security group ID for the django"
  type        = string
}
