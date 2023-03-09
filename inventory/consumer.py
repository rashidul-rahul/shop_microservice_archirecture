import time
from main import redis, Product


key = "order_completed"
group = "inventory-group"

try:
    redis.xgroup_create(key, group)
except Exception as _:
    print("Group already exist!")


while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        if results != []:
            for result in results:
                data = result[1][0][1]
                product = Product.get(data["product_id"])
                product.quantity = product.quantity - int(data["quantity"])
                product.save()
    except Exception as e:
        print(str(e))
    time.sleep(1)
