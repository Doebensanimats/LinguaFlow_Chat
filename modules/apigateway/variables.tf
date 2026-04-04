variable "region" {
  description = "AWS region"
  type        = string
}

variable "lambda_invoke_arn" {
  description = "Lambda function ARN to integrate with API Gateway"
  type        = string
}

variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
}