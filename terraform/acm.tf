data "aws_acm_certificate" "orders_api" {
  domain      = var.environment == "prod" ? "orders-api.megsparadisecakes.com" : "orders-dev-api.megsparadisecakes.com"
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}
