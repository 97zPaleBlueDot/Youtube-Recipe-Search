# resources
resource "aws_instance" "bastion_host" {
  ami                         = "ami-0075013580f6322a1"
  instance_type               = "t2.micro"
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [var.django_sg_id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.deployer2.key_name

  tags = {
    Name = "bastion_host"
  }
}

resource "aws_instance" "django_instance2" {
  ami                         = "ami-0075013580f6322a1"
  instance_type               = "t2.micro"
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [var.django_sg_id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.deployer2.key_name

  tags = {
    Name = "django_server2"
  }
}

resource "aws_instance" "ES_test_instance" {
  ami                         = "ami-0075013580f6322a1"
  instance_type               = "t2.micro"
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [var.django_sg_id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.deployer2.key_name

  tags = {
    Name = "ES_test_instance"
  }
}

# SSH key gen
resource "tls_private_key" "main_key_pair" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "deployer2" {
  key_name   = "deployer2-key"
  public_key = tls_private_key.main_key_pair.public_key_openssh
}

resource "local_file" "private_key" {
  content         = tls_private_key.main_key_pair.private_key_pem
  filename        = "${path.module}/files/deployer2-key.pem"
  file_permission = "0600"
}