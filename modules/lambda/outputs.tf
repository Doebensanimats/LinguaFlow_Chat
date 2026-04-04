output "lambda_arn" {
  description = "Full Lambda ARN for API Gateway"
  value       = aws_lambda_function.translate.arn
}

output "lambda_invoke_arn" {
  description = "Lambda Invoke ARN (for SDK or CLI)"
  value       = aws_lambda_function.translate.invoke_arn
}

output "function_name" {
  value = aws_lambda_function.translate.function_name
}