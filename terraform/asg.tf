# Grants the EC2 service permission to assume IAM role
data "aws_iam_policy_document" "ec2_trust" {
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

resource "aws_iam_role" "ec2" {
  name = "${local.project_name}-EC2"

  assume_role_policy = data.aws_iam_policy_document.ec2_trust.json

  tags = {
    Name = "${local.project_name}-EC2"
  }
}

resource "aws_iam_role_policy_attachment" "ec2_AmazonEC2ContainerRegistryReadOnly" {
  role       = aws_iam_role.ec2.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "ec2_AmazonS3FullAccess" {
  role       = aws_iam_role.ec2.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "ec2_AmazonRDSFullAccess" {
  role       = aws_iam_role.ec2.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${local.project_name}-EC2"

  path = "/"
  role = aws_iam_role.ec2.name
}

resource "aws_security_group" "ec2" {
  name        = "${local.project_name}-EC2"
  description = "Security group for EC2"

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project_name}-EC2"
  }
}

# Allow all ingress traffic only inside our VPC
resource "aws_security_group_rule" "asg_allow_internal_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = [aws_vpc.main.cidr_block]
}

# Allow all egress traffic
resource "aws_security_group_rule" "asg_allow_all_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.ec2.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

# Key pair for node so we can login via SSH
resource "aws_key_pair" "ec2" {
  key_name = "${local.project_name}-EC2"

  public_key = file("bastion_key.pub")

  tags = {
    Name = "${local.project_name}-EC2"
  }
}

data "aws_ami" "ubuntu_linux" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"]
  }
  owners = ["099720109477"]
}

resource "aws_launch_template" "ec2" {
  name        = "${local.project_name}-EC2"
  description = "EC2 instances"

  image_id               = data.aws_ami.ubuntu_linux.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.ec2.key_name
  vpc_security_group_ids = [aws_security_group.ec2.id]

  user_data = base64encode(
    templatefile(
      "user_data.sh",
      {
        aws_region            = var.aws_region,
        aws_access_key_id     = var.aws_access_key_id,
        server_port           = tostring(var.server_port),
        aws_secret_access_key = var.aws_secret_access_key,
        aws_repo_url          = aws_ecr_repository.app.repository_url,
        aws_registry_url      = split("/", aws_ecr_repository.app.repository_url)[0]
    })
  )

  iam_instance_profile {
    arn = aws_iam_instance_profile.ec2.arn
  }

  tags = {
    Name = "${local.project_name}-EC2"
  }
}

resource "aws_autoscaling_group" "ec2" {
  name = "${local.project_name}-EC2"

  desired_capacity          = var.asg_desired_capacity
  max_size                  = var.asg_max_size
  min_size                  = var.asg_min_size
  health_check_grace_period = var.asg_health_check_grace_period

  target_group_arns = [aws_lb_target_group.asg.arn]

  vpc_zone_identifier = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  launch_template {
    id      = aws_launch_template.ec2.id
    version = aws_launch_template.ec2.latest_version
  }

  //noinspection HCLUnknownBlockType
  instance_refresh {
    # Enable instances rolling update when some launch template parameters changes
    strategy = "Rolling"
    //noinspection HCLUnknownBlockType
    preferences {
      instance_warmup        = var.asg_rolling_instance_warmup
      min_healthy_percentage = var.asg_rolling_min_healthy_percentage
    }
  }

  tag {
    key                 = "Name"
    value               = local.project_name
    propagate_at_launch = true
  }
}
