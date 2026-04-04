variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "lambda_role_arn" {
  description = "IAM role ARN for Lambda"
  type        = string
}

# Add this variable to accept SQS queue URL
variable "sqs_queue_url" {
  description = "Optional: SQS queue URL for Lambda"
  type        = string
  default     = ""
}