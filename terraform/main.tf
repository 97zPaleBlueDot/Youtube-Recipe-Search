module "vpc" {
  source                = "./vpc"
  availability_zoneA    = var.availability_zoneA
  availability_zoneB    = var.availability_zoneB
  public_cidr           = var.public_cidr
  vpc_cidr              = var.vpc_cidr
  public_subnet_cidr    = var.public_subnet_cidr
  private_subnet_1_cidr = var.private_subnet_1_cidr
  private_subnet_2_cidr = var.private_subnet_2_cidr
}

module "security_groups" {
  source = "./security_groups"
  vpc_id = module.vpc.vpc_id
  public_cidr = var.public_cidr
  vpc_cidr    = var.vpc_cidr
}

module "instances" {
  source = "./instances"
  # subnets
  public_subnet_id  = module.vpc.public_subnet_id
  private_subnet_id = module.vpc.private_subnet_1_id
  # security_groups
  public_sg_id  = module.security_groups.public_sg_id
  private_sg_id = module.security_groups.private_sg_id
  django_sg_id  = module.security_groups.django_sg_id
}

module "rds" {
  source              = "./rds"
  private_subnet_1_id = module.vpc.private_subnet_1_id
  private_subnet_2_id = module.vpc.private_subnet_2_id
  rds_sg_id           = module.security_groups.rds_sg_id
  db_username         = var.db_username
  db_password         = var.db_password
}