data "aws_ecr_repository" "orders_api_lambdas" {
  name = var.environment == "prod" ? "orders-api-lambdas-us-east-1" : "dev-orders-api-lambdas-us-east-1"
}
