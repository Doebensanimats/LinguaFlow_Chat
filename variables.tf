variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "input_bucket_name" {}
variable "responses_bucket_name" {}
variable "lambda_role_name" {
  type    = string
  default = "translation-lambda-role"
}