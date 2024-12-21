locals {
  lambda_image = "${data.aws_ecr_repository.orders_api_lambdas.repository_url}:${var.docker_image_tag}"
}

resource "aws_lambda_function" "app" {
  image_uri     = local.lambda_image
  package_type  = "Image"
  function_name = "orders-api-us-east-1"
  role          = aws_iam_role.orders_api_role.arn

  timeout     = 30
  memory_size = 1024

  image_config {
    command = ["src.api.lambda_handler"]
  }

  environment {
    variables = {
      DYNAMODB_REGION                      = "us-east-1"
      DYNAMODB_ENDPOINT_URL                = "https://dynamodb.us-east-1.amazonaws.com"
      DYNAMODB_ORDERS_TABLE_NAME           = aws_dynamodb_table.orders.name
      DYNAMODB_ORDER_TYPE_COUNT_TABLE_NAME = aws_dynamodb_table.order_type_count.name
      DYNAMODB_PRICES_TABLE_NAME           = data.aws_dynamodb_table.prices.name
      REGION                               = "us-east-1",
    }
  }
}


