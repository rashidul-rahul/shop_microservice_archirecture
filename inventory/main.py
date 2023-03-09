from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel


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


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


def formant_product(pk: str):
    product = Product.get(pk)

    return {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
            }


@app.get('/all/products')
def get_products():
    return [formant_product(pk) for pk in Product.all_pks()]


@app.post("/product")
def create_product(product: Product):
    return product.save()


@app.get("/product/{pk}")
def geg_product(pk: str):
    return formant_product(pk)


@app.delete("/product/{pk}")
def delete_product(pk: str):
    return Product.delete(pk)
