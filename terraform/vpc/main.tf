# VPC settings
resource "aws_vpc" "main_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "dot-main"
  }
}

# Network ACL
resource "aws_network_acl" "main" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "main-network-acl"
  }
}
resource "aws_network_acl_rule" "allow_all_inbound" {
  network_acl_id = aws_network_acl.main.id
  rule_number    = 100
  egress         = false
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = var.public_cidr
}

resource "aws_network_acl_rule" "allow_all_outbound" {
  network_acl_id = aws_network_acl.main.id
  rule_number    = 100
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = var.public_cidr
}

# Subnet
# Public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = var.public_subnet_cidr
  availability_zone = var.availability_zoneA

  tags = {
    Name = "public_subnet-1"
  }
}
#Private subnet
resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = var.private_subnet_1_cidr
  availability_zone = var.availability_zoneA

  tags = {
    Name = "private_subnet-1"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = var.private_subnet_2_cidr
  availability_zone = var.availability_zoneB

  tags = {
    Name = "private_subnet-2"
  }
}


# elastic ip 
resource "aws_eip" "nat_1" {
  domain = "vpc"

  lifecycle {
    create_before_destroy = true
  }
}
# NAT gateway
resource "aws_nat_gateway" "nat_gateway_private" {
  allocation_id = aws_eip.nat_1.id
  subnet_id     = aws_subnet.public_subnet.id

  tags = {
    Name = "NAT-GW-1"
  }
}
# internet gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "main"
  }
}
# ROUTE TABLES
# public ROUTE TABLE
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = var.public_cidr
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "main-1"
  }
}
# Private ROUTE TABLE
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block     = var.public_cidr
    nat_gateway_id = aws_nat_gateway.nat_gateway_private.id
  }

  tags = {
    Name = "main-private-1"
  }
}

# association
resource "aws_route_table_association" "route_table_association_1" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "route_table_association_private_1" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_route_table.id
}
resource "aws_route_table_association" "route_table_association_private_2" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_route_table.id
}

# Subnet Network ACL Association
resource "aws_network_acl_association" "public_association" {
  subnet_id      = aws_subnet.public_subnet.id
  network_acl_id = aws_network_acl.main.id
}

resource "aws_network_acl_association" "private_1_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  network_acl_id = aws_network_acl.main.id
}

resource "aws_network_acl_association" "private_2_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  network_acl_id = aws_network_acl.main.id
}