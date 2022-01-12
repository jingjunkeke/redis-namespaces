# python3.8
# -*- coding: utf-8 -*-
# @CreateTime    : 2022/1/12 14:19
# @Author  : JingJunKe
# @File    : test.py
# @Software: PyCharm
import redis
from redis_namespace import StrictRedis

# redis_connection = redis.StrictRedis()
namespaced_redis = StrictRedis(host='127.0.0.1', port='6379', namespace='ns:')
namespaced_redis.set('foo', 'bar')  # redis_connection.set('ns:foo', 'bar')
print(namespaced_redis.get('foo'))
# namespaced_redis.get('foo')
# namespaced_redis.get('foo')

