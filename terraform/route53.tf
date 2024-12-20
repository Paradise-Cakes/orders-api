data "aws_route53_zone" "orders_api" {
  name = var.environment == "prod" ? "orders-api.megsparadisecakes.com" : "orders-dev-api.megsparadisecakes.com"
}

data "aws_route53_zone" "paradise_cakes" {
  name = var.environment == "prod" ? "megsparadisecakes.com" : "dev.megsparadisecakes.com"
}
