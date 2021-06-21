resource "aws_ssm_parameter" "app_port" {
  name        = "/picture-uploader/env/PICTURE_UPLOADER_PORT"
  type        = "String"
  value       = var.server_port
}

resource "aws_ssm_parameter" "app_is_reload" {
  name        = "/picture-uploader/env/PICTURE_UPLOADER_IS_RELOAD"
  type        = "String"
  value       = 1
}

resource "aws_ssm_parameter" "app_num_workers" {
  name        = "/picture-uploader/env/PICTURE_UPLOADER_NUM_WORKERS"
  type        = "String"
  value       = 2
}

resource "aws_ssm_parameter" "app_num_threads" {
  name        = "/picture-uploader/env/PICTURE_UPLOADER_NUM_THREADS"
  type        = "String"
  value       = 2
}

resource "aws_ssm_parameter" "db_work_user" {
  name        = "/picture-uploader/env/POSTGRES_WORK_USER"
  type        = "SecureString"
  value       = var.db_username
}

resource "aws_ssm_parameter" "db_work_db" {
  name        = "/picture-uploader/env/POSTGRES_WORK_DB"
  type        = "SecureString"
  value       = "picture_db"
}

resource "aws_ssm_parameter" "db_work_user_password" {
  name        = "/picture-uploader/env/POSTGRES_WORK_USER_PASSWORD"
  type        = "SecureString"
  value       = var.db_password
}

resource "aws_ssm_parameter" "db_host" {
  name        = "/picture-uploader/env/POSTGRES_HOST"
  type        = "String"
  value       = aws_db_instance.main.address
}

resource "aws_ssm_parameter" "db_port" {
  name        = "/picture-uploader/env/POSTGRES_PORT"
  type        = "String"
  value       = 5432
}

resource "aws_ssm_parameter" "db_driver" {
  name        = "/picture-uploader/env/POSTGRES_ALCHEMY_DRIVER"
  type        = "String"
  value       = "postgresql+psycopg2"
}

resource "aws_ssm_parameter" "bucket_name" {
  name        = "/picture-uploader/env/S3_BUCKET_NAME"
  type        = "String"
  value       = aws_s3_bucket.main.bucket
}
