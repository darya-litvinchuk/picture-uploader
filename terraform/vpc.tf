resource "aws_vpc" "main" {
  cidr_block = var.cidr_block

  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = "${local.project_name}-Network"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project_name}-IGW"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project_name}-PublicRouteTable"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project_name}-PrivateRouteTable-A"
  }
}

resource "aws_route_table" "db" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project_name}-DbRouteTable"
  }
}

resource "aws_route" "public_igw" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

resource "aws_route" "private_nat" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main.id
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_a_cidr_block
  availability_zone       = local.az_a
  map_public_ip_on_launch = true

  tags = {
    Name = "${local.project_name}-PublicSubnet-A"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_b_cidr_block
  availability_zone       = local.az_b
  map_public_ip_on_launch = true

  tags = {
    Name = "${local.project_name}-PublicSubnet-B"
  }
}

resource "aws_subnet" "private_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_a_cidr_block
  availability_zone       = local.az_a
  map_public_ip_on_launch = false

  tags = {
    Name = "${local.project_name}-PrivateSubnet-A"
  }
}

resource "aws_subnet" "private_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_b_cidr_block
  availability_zone       = local.az_b
  map_public_ip_on_launch = false

  tags = {
    Name = "${local.project_name}-PrivateSubnet-B"
  }
}

resource "aws_subnet" "db_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.db_subnet_a_cidr_block
  availability_zone       = local.az_a
  map_public_ip_on_launch = false

  tags = {
    Name = "${local.project_name}-DbSubnet-A"
  }
}

resource "aws_subnet" "db_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.db_subnet_b_cidr_block
  availability_zone       = local.az_b
  map_public_ip_on_launch = false

  tags = {
    Name = "${local.project_name}-DbSubnet-A"
  }
}

resource "aws_eip" "nat" {
  vpc = true

  tags = {
    Name = "${local.project_name}-EIP-A"
  }

  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_a.id

  tags = {
    Name = "${local.project_name}-NatGateway-A"
  }

  depends_on = [aws_internet_gateway.main]
}

resource "aws_route_table_association" "public_a" {
  route_table_id = aws_route_table.public.id
  subnet_id      = aws_subnet.public_a.id
}

resource "aws_route_table_association" "public_b" {
  route_table_id = aws_route_table.public.id
  subnet_id      = aws_subnet.public_b.id
}

resource "aws_route_table_association" "private_a" {
  route_table_id = aws_route_table.private.id
  subnet_id      = aws_subnet.private_a.id
}

resource "aws_route_table_association" "private_b" {
  route_table_id = aws_route_table.private.id
  subnet_id      = aws_subnet.private_b.id
}

resource "aws_route_table_association" "db_a" {
  route_table_id = aws_route_table.db.id
  subnet_id = aws_subnet.db_a.id
}

resource "aws_route_table_association" "db_b" {
  route_table_id = aws_route_table.db.id
  subnet_id = aws_subnet.db_b.id
}
