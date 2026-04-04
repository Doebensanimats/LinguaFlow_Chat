output "input_bucket_arn" {
  value = module.s3.input_bucket_arn
}

output "responses_bucket_arn" {
  value = module.s3.responses_bucket_arn
}

output "lambda_invoke_arn" {
  value = module.lambda.lambda_invoke_arn
}

output "api_url" {
  value = module.apigateway.api_url
}

output "sqs_queue_url" {
  value = module.sqs.sqs_queue_url
}