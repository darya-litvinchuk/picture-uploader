resource "aws_s3_bucket" "main" {
  bucket = local.project_name
  acl    = "private"

  tags = {
    Name = local.project_name
  }
}
