from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel


app = FastAPI()

redis = get_redis_connection(
        host="",
        port="",
        password="",
        decode_responses=True
        )


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def get_products():
    return []
