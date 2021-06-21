resource "aws_db_subnet_group" "main" {
  name       = local.project_name
  subnet_ids = [aws_subnet.db_a.id, aws_subnet.db_b.id]

  tags = {
    Name = local.project_name
  }
}

resource "aws_db_parameter_group" "main" {
  name   = local.project_name
  family = "postgres12"

}

resource "aws_security_group" "rds" {
  name        = "${local.project_name}-RDS"
  description = "Security group for RDS"

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project_name}-RDS"
  }
}

resource "aws_security_group_rule" "rds_allow_internal_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.rds.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = [aws_vpc.main.cidr_block]
}

resource "aws_security_group_rule" "rds_allow_all_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.rds.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_db_instance" "main" {
  identifier           = local.project_name
  instance_class       = "db.t2.micro"
  allocated_storage    = 5
  engine               = "postgres"
  engine_version       = "12.5"
  username             = var.db_username
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name = aws_db_parameter_group.main.name
  publicly_accessible  = true
  skip_final_snapshot  = true
  multi_az             = false
}
