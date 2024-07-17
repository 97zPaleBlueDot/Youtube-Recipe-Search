variable "availability_zoneA" {
  description = "The availability zone for the first public subnet"
  type        = string
}

variable "availability_zoneB" {
  description = "The availability zone for the second public subnet"
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