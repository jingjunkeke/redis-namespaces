# redis-namespaces

***
redis-namespaces 为 redis.Redis 添加了类装饰器，在类装饰器中，又为每个操作 key 的方法设置了函数装饰器，函数装饰器拦截方法调用，给操作 key 的 name 添加统一前缀 namespace ;

### 示例：

```python
from redis import Redis
from redis_namespaces import Redis as RedisNS

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