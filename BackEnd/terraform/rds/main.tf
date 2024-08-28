resource "aws_db_instance" "default" {
  allocated_storage      = 50
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "12.18"
  instance_class         = "db.t3.micro"
  db_name                = "main_rds"
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = "default.postgres12"
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [var.rds_sg_id]
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds_subnet_group"
  subnet_ids = [var.private_subnet_1_id, var.private_subnet_2_id]

  tags = {
    Name = "rds_subnet_group"
  }
}
