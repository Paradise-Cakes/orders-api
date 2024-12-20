locals {
  lambda_image = "${data.aws_ecr_repository.orders_api_lambdas.repository_url}:${var.docker_image_tag}"
}

resource "aws_lambda_function" "app" {
  image_uri     = local.lambda_image
  package_type  = "Image"
  function_name = var.environment == "prod" ? "orders-api-us-east-1" : "dev-orders-api-us-east-1"
  role          = aws_iam_role.orders_api_role.arn

  timeout     = 30
  memory_size = 1024

  image_config {
    command = ["src.api.lambda_handler"]
  }

  environment {
    variables = {
      REGION = "us-east-1"
    }
  }
}


