import time
from main import redis, Product


key = "order_completed"
group = "inventory-group"

try:
    redis.xgroup_create(key, group)
except Exception:
    print("Group already exist!")


while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        if results != []:
            for result in results:
                data = result[1][0][1]
                try:
                    product = Product.get(data["product_id"])
                    product.quantity = product.quantity - int(data["quantity"])
                    product.save()
                    print("product save")
                except Exception:
                    print("call delete")
                    redis.xadd("order_deleted", data, "*")

    except Exception as e:
        print(str(e))
    time.sleep(1)
