# redis-namespaces

***
redis-namespaces 和 redis-py 的唯一不同之处是：redis-namespaces 给 redis 的函数加上了装饰器，给所有操作都加上了 name (key) 的统一的前缀。

### 示例：

```python
from redis import Redis
from redis_namespaces import RedisNS

namespaced_redis = RedisNS(namespace='namespace')
namespaced_redis.set(name='age', values='bar')  # name='namespace:age'
values_1 = namespaced_redis.get(name='age')  # name='namespace:age'

redis_connection = Redis()
values_2 = redis_connection.get('namespace:age')

print(values_1 == values_2)  # True
```

### 安装 Installation

```shell
pip install redis-namespaces
```

### 注意：redis-namespaces 版本 必须 和 redis-py 版本一致
| redis | redis-namespaces |
|-------|------------------|
| 4.1.0 | 4.1.0.1          |