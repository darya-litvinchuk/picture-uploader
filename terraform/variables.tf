variable "cidr_block" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_a_cidr_block" {
  description = "The CIDR block for the public subnet A"
  type        = string
  default     = "10.0.11.0/24"
}

variable "public_subnet_b_cidr_block" {
  description = "The CIDR block for the public subnet B"
  type        = string
  default     = "10.0.21.0/24"
}

variable "private_subnet_a_cidr_block" {
  description = "The CIDR block for the private subnet"
  type        = string
  default     = "10.0.12.0/24"
}

variable "private_subnet_b_cidr_block" {
  description = "The CIDR block for the private subnet"
  type        = string
  default     = "10.0.14.0/24"
}

variable "db_subnet_a_cidr_block" {
  description = "The CIDR block for the db subnet"
  type        = string
  default     = "10.0.13.0/24"
}

variable "db_subnet_b_cidr_block" {
  description = "The CIDR block for the db subnet"
  type        = string
  default     = "10.0.100.0/24"
}

variable "instance_type" {
  description = "The EC2 instance type"
  type        = string
  default     = "t3.nano"
}


variable "allowed_bastion_ip" {
  description = "The IP address that has access for bastion"
  type        = string
}

variable "asg_desired_capacity" {
  description = "Desired capacity of EC2 ASG"
  type        = number
  default     = 2
}

variable "asg_min_size" {
  description = "Minimum size of node ASG"
  type        = number
  default     = 1
}

variable "asg_max_size" {
  description = "Maximum size of node ASG"
  type        = number
  default     = 3
}

variable "asg_health_check_grace_period" {
  description = "Time (in seconds) after instance comes into service before checking health"
  type        = number
  default     = 60
}

variable "asg_rolling_min_healthy_percentage" {
  description = "Min healthy percentage of nodes during rolling update"
  type        = number
  default     = 50
}

variable "asg_rolling_instance_warmup" {
  description = "The number of seconds until a newly launched instance is configured and ready to use"
  type        = number
  default     = 60
}

variable "server_port" {
  description = "Application server port"
  type        = number
  default     = 8008
}

variable "healthcheck_endpoint" {
  description = "Application healthcheck endpoint"
  type        = string
  default     = "/api/v1/picture-uploader/healthcheck"
}

variable "db_username" {
  description = "Database administrator username"
  type        = string
  default     = "picture_uploader"
  sensitive   = true
}

variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

variable "aws_access_key_id" {
  description = "AWS access key id"
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "AWS region name"
  type        = string
  default     = "us-east-1"
}
