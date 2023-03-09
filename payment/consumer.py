import time
from main import redis, Order


key = "order_deleted"
group = "payment-group"

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
                order = Order.get(data["pk"])
                order.status = "refunded"
                order.save()
    except Exception as e:
        print(str(e))
    time.sleep(1)
