
variable "db_username" {
  description = "The username for the RDS instance"
  type        = string
}

variable "db_password" {
  description = "The password for the RDS instance"
  type        = string
}

variable "private_subnet_1_id" {
  description = "The first private subnet ID where the RDS will be created"
  type        = string
}

variable "private_subnet_2_id" {
  description = "The second private subnet ID where the RDS will be created"
  type        = string
}

variable "rds_sg_id" {
  description = "The security group ID for the RDS instance"
  type        = string
}