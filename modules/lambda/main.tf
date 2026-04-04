data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "translate" {
  function_name = var.function_name
  role          = var.lambda_role_arn
  handler       = "lambda_function.lambda_handler"  
  runtime       = "python3.11"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  environment {
    variables = {
      SQS_QUEUE_URL = var.sqs_queue_url
    }
  }
}