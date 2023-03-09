import time
import httpx
from fastapi import FastAPI
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from fastapi.background import BackgroundTasks


app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=['*'],
        allow_headers=['*']
        )

redis = get_redis_connection(
        host="redis-19644.c1.ap-southeast-1-1.ec2.cloud.redislabs.com",
        port="19644",
        password="E6fzwFJ9sTjXZUGVBSr9uOuLFWztyk6m",
        decode_responses=True
        )

PRODUCT_FEE: float = .02


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, complete, refunded, declined

    class Meta:
        database = redis


def order_completed(order: Order):
    time.sleep(5)
    order.status = "complete"
    order.save()
    redis.xadd("order_completed", order.dict(), "*")


@app.post("/order/create")
async def create_order(request: Request, backgroaud_task: BackgroundTasks):
    data = await request.json()
    resp = httpx.request("GET", f"http://localhost:8000/product/{data['product_id']}")
    if resp.status_code == 200:
        product = resp.json()
    else:
        resp.raise_for_status()
    fee = PRODUCT_FEE * float(product["price"])
    total = fee + float(product["price"])
    order = Order(
            product_id=product["id"],
            price=product["price"],
            fee=fee,
            total=total,
            quantity=data["quantity"],
            status="pending"
                        )

    backgroaud_task.add_task(order_completed, order)
    return order


@app.get("/order/{pk}")
def get_order(pk: str):
    return Order.get(pk)
