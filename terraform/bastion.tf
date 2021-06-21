# Grants the EC2 service permission to assume IAM role
data "aws_iam_policy_document" "bastion_trust" {
  version = "2012-10-17"

  statement {
    effect = "Allow"
    principals {
      identifiers = ["ec2.amazonaws.com"]
      type        = "Service"
    }
    actions = [
      "sts:AssumeRole"
    ]
  }
}

resource "aws_iam_role" "bastion" {
  name = "${local.project_name}-BastionIAMRole"

  assume_role_policy = data.aws_iam_policy_document.bastion_trust.json

  tags = {
    Name = "${local.project_name}-BastionIAMRole"
  }
}

resource "aws_iam_instance_profile" "bastion" {
  name = "${local.project_name}-BastionIAMInstanceProfile"

  path = "/"
  role = aws_iam_role.bastion.name
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-2.0.*-x86_64-gp2"]
  }
  owners = ["amazon"]
}

resource "aws_security_group" "bastion" {
  name        = "${local.project_name}-BastionSecurityGroup"
  description = "Security group for bastion host"

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project_name}-BastionSecurityGroup"
  }
}

# Allow ingress SSH access to bastion
resource "aws_security_group_rule" "allow_ssh_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.bastion.id

  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = [var.allowed_bastion_ip]
}

# Allow egress SSH access from bastion only within our VPC
resource "aws_security_group_rule" "allow_ssh_node_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.bastion.id

  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = [aws_vpc.main.cidr_block]
}

# Key pair for bastion so we can login via SSH
resource "aws_key_pair" "bastion" {
  key_name = "${local.project_name}-BastionKeyPair"

  public_key = file("bastion_key.pub")

  tags = {
    Name = "${local.project_name}-BastionKeyPair"
  }
}

resource "aws_instance" "bastion" {
  ami                    = data.aws_ami.amazon_linux.id
  availability_zone      = local.az_b
  instance_type          = var.instance_type
  key_name               = aws_key_pair.bastion.key_name
  subnet_id              = aws_subnet.public_b.id
  iam_instance_profile   = aws_iam_instance_profile.bastion.name
  vpc_security_group_ids = [aws_security_group.bastion.id]

  tags = {
    Name = "${local.project_name}-Bastion"
  }
}
