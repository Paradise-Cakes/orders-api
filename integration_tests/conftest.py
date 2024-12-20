import os
import uuid

import boto3
import pytest
from dotenv import load_dotenv
from request_helper import RequestHelper

load_dotenv()


@pytest.fixture(scope="session")
def api_url():
    local_port = os.getenv("LOCAL_PORT")

    if local_port:
        return f"http://localhost:{local_port}"

    return "https://orders-dev-api.megsparadisecakes.com"


@pytest.fixture(scope="session")
def request_helper(api_url):
    return RequestHelper(api_url, {})


@pytest.fixture(scope="session")
def dynamodb_client():
    return boto3.client("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="function")
def function_prices(dynamodb_client, cleanup_prices):
    def _create_prices(dessert_id):
        records = [
            {
                "dessert_id": {"S": dessert_id},
                "size": {"S": "slice"},
                "base_price": {"N": "5.00"},
                "discount": {"N": "0.00"},
            },
            {
                "dessert_id": {"S": dessert_id},
                "size": {"S": "whole"},
                "base_price": {"N": "40.00"},
                "discount": {"N": "0.00"},
            },
        ]

        for record in records:
            dynamodb_client.put_item(
                TableName="prices",
                Item=record,
            )
        cleanup_prices.extend(records)

        return {"dessert_id": dessert_id, "records": records}

    return _create_prices


@pytest.fixture(scope="function")
def function_orders(dynamodb_client, cleanup_orders):
    order_ids = [
        f"ORDER-{str(uuid.uuid4())}",
        f"ORDER-{str(uuid.uuid4())}",
        f"ORDER-{str(uuid.uuid4())}",
    ]

    records = [
        {
            "order_id": {"S": order_ids[0]},
            "customer_first_name": {"S": "John"},
            "customer_last_name": {"S": "Cena"},
            "customer_full_name": {"S": "John Cena"},
            "customer_email": {"S": "john.cena@gmail.com"},
            "customer_phone_number": {"S": "1234567890"},
            "delivery_zip_code": {"S": "12345"},
            "delivery_address_line_1": {"S": "123 Main St"},
            "delivery_address_line_2": {"S": "Apt 1"},
            "delivery_date": {"S": "01-01-2022"},
            "delivery_time": {"N": "12"},
            "order_status": {"S": "NEW"},
            "order_date": {"S": "12-31-2021"},
            "order_time": {"N": "12"},
            "approved": {"BOOL": False},
            "custom_order": {"BOOL": False},
            "order_total": {"N": "0.00"},
            "desserts": {
                "L": [
                    {
                        "M": {
                            "dessert_id": {"S": "DESSERT-1"},
                            "dessert_name": {"S": "Chocolate Cake"},
                            "size": {"S": "slice"},
                            "quantity": {"N": "2"},
                        }
                    }
                ]
            },
            "last_updated_at": {"N": "1734036429"},
        },
        {
            "order_id": {"S": order_ids[1]},
            "customer_first_name": {"S": "Jane"},
            "customer_last_name": {"S": "Doe"},
            "customer_full_name": {"S": "Jane Doe"},
            "customer_email": {"S": "jane.doe@gmail.com"},
            "customer_phone_number": {"S": "0987654321"},
            "delivery_zip_code": {"S": "54321"},
            "delivery_address_line_1": {"S": "456 Elm St"},
            "delivery_address_line_2": {"S": "Apt 2"},
            "delivery_date": {"S": "02-02-2022"},
            "delivery_time": {"N": "14"},
            "order_status": {"S": "NEW"},
            "order_date": {"S": "01-02-2022"},
            "order_time": {"N": "14"},
            "approved": {"BOOL": False},
            "custom_order": {"BOOL": False},
            "order_total": {"N": "0.00"},
            "desserts": {
                "L": [
                    {
                        "M": {
                            "dessert_id": {"S": "DESSERT-2"},
                            "dessert_name": {"S": "Cheesecake"},
                            "size": {"S": "whole"},
                            "quantity": {"N": "1"},
                        }
                    }
                ]
            },
            "last_updated_at": {"N": "1734036429"},
        },
        {
            "order_id": {"S": order_ids[2]},
            "customer_first_name": {"S": "James"},
            "customer_last_name": {"S": "Bond"},
            "customer_full_name": {"S": "James Bond"},
            "customer_email": {"S": "james.bond@gmail.com"},
            "customer_phone_number": {"S": "1357924680"},
            "delivery_zip_code": {"S": "67890"},
            "delivery_address_line_1": {"S": "789 Oak St"},
            "delivery_address_line_2": {"S": "Apt 3"},
            "delivery_date": {"S": "03-02-2023"},
            "delivery_time": {"N": "16"},
            "order_status": {"S": "NEW"},
            "order_date": {"S": "03-02-2023"},
            "order_time": {"N": "16"},
            "approved": {"BOOL": False},
            "custom_order": {"BOOL": False},
            "order_total": {"N": "0.00"},
            "desserts": {
                "L": [
                    {
                        "M": {
                            "dessert_id": {"S": "DESSERT-3"},
                            "dessert_name": {"S": "Carrot Cake"},
                            "size": {"S": "slice"},
                            "quantity": {"N": "3"},
                        }
                    }
                ]
            },
            "last_updated_at": {"N": "1734036429"},
        },
    ]

    cleanup_orders.extend(order_ids)

    for record in records:
        dynamodb_client.put_item(
            TableName="orders",
            Item=record,
        )

    return {"order_ids": order_ids, "records": records}


@pytest.fixture(scope="function")
def function_order(dynamodb_client, cleanup_orders):
    def _get_order_record(delivery_date="01-01-2022"):
        order_id = f"ORDER-{str(uuid.uuid4())}"

        record = {
            "order_id": {"S": order_id},
            "customer_first_name": {"S": "John"},
            "customer_last_name": {"S": "Cena"},
            "customer_full_name": {"S": "John Cena"},
            "customer_email": {"S": "john.cena@gmail.com"},
            "customer_phone_number": {"S": "1234567890"},
            "delivery_zip_code": {"S": "12345"},
            "delivery_address_line_1": {"S": "123 Main St"},
            "delivery_address_line_2": {"S": "Apt 1"},
            "delivery_date": {"S": delivery_date},
            "delivery_time": {"N": "12"},
            "order_status": {"S": "NEW"},
            "order_date": {"S": "12-31-2021"},
            "order_time": {"N": "12"},
            "approved": {"BOOL": False},
            "custom_order": {"BOOL": False},
            "order_total": {"N": "0.00"},
            "desserts": {
                "L": [
                    {
                        "M": {
                            "dessert_id": {"S": "DESSERT-1"},
                            "dessert_name": {"S": "Chocolate Cake"},
                            "size": {"S": "slice"},
                            "quantity": {"N": "2"},
                        }
                    }
                ]
            },
            "last_updated_at": {"N": "1734036429"},
        }

        dynamodb_client.put_item(
            TableName="orders",
            Item=record,
        )

        cleanup_orders.append(order_id)

        return {"order_id": order_id, "record": record}

    return _get_order_record


@pytest.fixture(scope="function")
def cleanup_orders(dynamodb_client):
    orders_to_cleanup = []
    yield orders_to_cleanup

    # Cleanup logic
    for order_id in orders_to_cleanup:
        try:
            dynamodb_client.delete_item(
                Key={
                    "order_id": {"S": order_id},
                },
                TableName="orders",
            )
            print(f"Deleted test order: {order_id}")
        except Exception as e:
            print(f"Failed to delete order {order_id}: {e}")
            raise e


@pytest.fixture(scope="function")
def cleanup_prices(dynamodb_client):
    prices_to_cleanup = []
    yield prices_to_cleanup

    for price in prices_to_cleanup:
        dessert_id = price.get("dessert_id").get("S")
        size = price.get("size").get("S")
        try:
            dynamodb_client.delete_item(
                Key={
                    "dessert_id": {"S": dessert_id},
                    "size": {"S": size},
                },
                TableName="prices",
            )
            print(f"Deleted test price: {dessert_id} - {size}")
        except Exception as e:
            print(f"Failed to delete price {dessert_id} - {size}: {e}")
            raise e
