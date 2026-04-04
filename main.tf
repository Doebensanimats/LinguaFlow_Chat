provider "aws" {
  region = var.aws_region
}

# --- S3 Buckets ---
module "s3" {
  source = "./modules/s3"

  input_bucket_name     = "translation-app-input-2026"
  responses_bucket_name = "translation-app-response-2026"
}

# --- SQS Queue ---
module "sqs" {
  source     = "./modules/sqs"
  queue_name = "translation-batch-queue"
}

# --- IAM Role for Lambda ---
module "iam" {
  source = "./modules/iam"

  role_name  = "translation-lambda-role"
  s3_buckets = [module.s3.input_bucket_arn, module.s3.responses_bucket_arn]
}

# --- Lambda Function ---
module "lambda" {
  source = "./modules/lambda"

  function_name   = "translation-lambda"
  lambda_role_arn = module.iam.lambda_role_arn
  sqs_queue_url   = module.sqs.sqs_queue_url
}

# --- API Gateway ---
module "apigateway" {
  source = "./modules/apigateway"

  region               = var.aws_region
  lambda_invoke_arn    = module.lambda.lambda_arn          
  lambda_function_name = module.lambda.function_name
}