# -*- coding: utf-8 -*-

from functools import wraps

from redis import Redis as _Rds

_DECO_FUNC = ['decr', 'decrby', 'dump', 'expire', 'expireat', 'geoadd', 'geodist', 'geohash', 'geopos', 'georadius',
              'georadiusbymember', 'geosearch', 'get', 'getbit', 'getdel', 'getex', 'getset', 'hdel', 'hexists', 'hget',
              'hgetall', 'hincrby', 'hincrbyfloat', 'hkeys', 'hlen', 'hmget', 'hmset', 'hscan', 'hscan_iter', 'hset',
              'hsetnx', 'hstrlen', 'hvals', 'incr', 'incrby', 'incrbyfloat', 'lindex', 'linsert', 'llen', 'lock',
              'lpop', 'lpos', 'lpush', 'lpushx', 'lrange', 'lrem', 'lset', 'ltrim', 'move', 'persist', 'pexpire',
              'pexpireat', 'pfadd', 'psetex', 'pttl', 'restore', 'rpop', 'rpush', 'rpushx', 'sadd', 'scard', 'set',
              'setbit', 'setex', 'setnx', 'setrange', 'sismember', 'smembers', 'smismember', 'sort', 'spop',
              'srandmember', 'srem', 'sscan', 'sscan_iter', 'strlen', 'substr', 'ttl', 'type', 'xack', 'xadd',
              'xautoclaim', 'xclaim', 'xdel', 'xgroup_create', 'xgroup_createconsumer', 'xgroup_delconsumer',
              'xgroup_destroy', 'xgroup_setid', 'xinfo_consumers', 'xinfo_groups', 'xinfo_stream', 'xlen', 'xpending',
              'xpending_range', 'xrange', 'xrevrange', 'xtrim', 'zadd', 'zcard', 'zcount', 'zincrby', 'zlexcount',
              'zpopmax', 'zpopmin', 'zrange', 'zrangebylex', 'zrangebyscore', 'zrank', 'zrem', 'zremrangebylex',
              'zremrangebyrank', 'zremrangebyscore', 'zrevrange', 'zrevrangebylex', 'zrevrangebyscore', 'zrevrank',
              'zscan', 'zscan_iter', 'zscore']


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
    """
    for attr in dir(redis_class):
        if attr in _DECO_FUNC:
            func = getattr(redis_class, attr)
            wrapped = _deco_redis_func(func)
            setattr(redis_class, attr, wrapped)
    return redis_class


@_deco_redis_class
class Redis(_Rds):
    """
    Use:
        redis_namespaces.Redis(namespace='namespace')
        or
        redis_namespaces.StrictRedis(namespace='namespace')
    """

    def __init__(self, namespace, *args, **kwargs):
        """
        Rewrite __init__ method
        :param namespace: Unified prefix
        :param *args, **kwargs: Refer to super().__init__(*args, **kwargs)
        """
        super().__init__(*args, **kwargs)
        self.namespace = namespace


StrictRedis = Redis
