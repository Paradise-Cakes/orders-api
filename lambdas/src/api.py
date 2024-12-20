from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from src.routes import get_order, get_orders, patch_order, post_order

app = FastAPI(title="Orders API", version="1.0.0", root_path="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_orders.router)
app.include_router(get_order.router)
app.include_router(post_order.router)
app.include_router(patch_order.router)


def lambda_handler(event, context):
    handler = Mangum(app, lifespan="on", api_gateway_base_path="/v1")
    return handler(event, context)
