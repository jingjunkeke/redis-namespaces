# python3.9
# -*- coding: utf-8 -*-
# @CreateTime    : 2021/12/20 16:02
# @Author  : JingJunKe
# @File    : redis-namespaces.py
# @Software: PyCharm
"""
对 redis-py 的封装
"""
from functools import wraps

from redis import Redis

DECO_FUNC = ['decr', 'decrby', 'dump', 'expire', 'expireat', 'geoadd', 'geodist', 'geohash', 'geopos', 'georadius',
             'georadiusbymember', 'geosearch', 'get', 'getbit', 'getdel', 'getex', 'getset', 'hdel', 'hexists', 'hget',
             'hgetall', 'hincrby', 'hincrbyfloat', 'hkeys', 'hlen', 'hmget', 'hmset', 'hscan', 'hscan_iter', 'hset',
             'hsetnx', 'hstrlen', 'hvals', 'incr', 'incrby', 'incrbyfloat', 'lindex', 'linsert', 'llen', 'lock', 'lpop',
             'lpos', 'lpush', 'lpushx', 'lrange', 'lrem', 'lset', 'ltrim', 'move', 'persist', 'pexpire', 'pexpireat',
             'pfadd', 'psetex', 'pttl', 'restore', 'rpop', 'rpush', 'rpushx', 'sadd', 'scard', 'set', 'setbit', 'setex',
             'setnx', 'setrange', 'sismember', 'smembers', 'smismember', 'sort', 'spop', 'srandmember', 'srem', 'sscan',
             'sscan_iter', 'strlen', 'substr', 'ttl', 'type', 'xack', 'xadd', 'xautoclaim', 'xclaim', 'xdel',
             'xgroup_create', 'xgroup_createconsumer', 'xgroup_delconsumer', 'xgroup_destroy', 'xgroup_setid',
             'xinfo_consumers', 'xinfo_groups', 'xinfo_stream', 'xlen', 'xpending', 'xpending_range', 'xrange',
             'xrevrange', 'xtrim', 'zadd', 'zcard', 'zcount', 'zincrby', 'zlexcount', 'zpopmax', 'zpopmin', 'zrange',
             'zrangebylex', 'zrangebyscore', 'zrank', 'zrem', 'zremrangebylex', 'zremrangebyrank', 'zremrangebyscore',
             'zrevrange', 'zrevrangebylex', 'zrevrangebyscore', 'zrevrank', 'zscan', 'zscan_iter', 'zscore']


def _deco_redis_func(redis_func):
    """
    It is essentially a function decorator
    Use setattr(class,func_str,_class_method_decorator) Decorative Redis methods
    :param redis_func: Redis methods
    """

    @wraps(redis_func)
    def wrapper(self, *args, **kwargs):
        if (name := kwargs.get('name')) is None:
            name, *args = args
            args.insert(0, f"{self.namespace}:{name}")
        else:
            kwargs['name'] = f"{self.namespace}:{name}"
        return redis_func(self, *args, **kwargs)

    return wrapper


def _deco_redis_class(redis_class):
    """
    Class decorator
    :param redis_class: class redis.Redis
    :return redis_class: be decorated class redis.Redis
    """
    for attr in dir(redis_class):
        if attr in DECO_FUNC:  # 对 name 参数做特殊处理
            func = getattr(redis_class, attr)
            wrapped = _deco_redis_func(func)
            setattr(redis_class, attr, wrapped)
    return redis_class


@_deco_redis_class
class RedisNS(Redis):
    """
    Redis-
    与原生父类 Redis 的唯一不同之处：
        1.给对象的 key 加上统一的前缀 namespace ; 目的是隔离每一个 key-value 空间; 防止冲突覆盖
    Use:
        znz_redis.RedisSon(namespace='foobar')
    """

    def __init__(self, namespace, *args, **kwargs):
        """详细参数注释见父类 Redis 源码"""
        super().__init__(*args, **kwargs)
        self.namespace = namespace


StrictRedisNS = RedisNS
