__REDIS_URL_KEY = "REDIS_URL"


def redis_decode(value):
    if isinstance(value, bytes):
        return value.decode('utf8')
    elif isinstance(value, (list, tuple, set)):
        return type(value)(map(redis_decode, value))
    else:
        return value


def redis_connect(url=None):
    if not url:
        from .zconfig import get_param
        url = get_param(__REDIS_URL_KEY)
    assert url
    return ZRedis(url)


class ZRedis:
    def __init__(self, url):
        import redis
        self.client = redis.from_url(url)

    def bpop_log(self, key, wait_log=None):
        if self.llen(key) <= 0:
            if wait_log:
                print(wait_log)
        return self.blpop(key)

    def get(self, key):
        return redis_decode(self.client.get(key))

    def set(self, key, value):
        return self.client.set(key, value)

    def expire(self, key, ttl):
        return self.client.expire(key, ttl)

    def set_expire(self, key, value, ttl):
        self.set(key, value)
        return self.expire(key, ttl)

    def rename(self, src, dst):
        self.client.rename(src, dst)

    def sall(self, key):
        return [redis_decode(it) for it in self.client.sunion(key)]

    def sadd(self, key, *value):
        return self.client.sadd(key, *value)

    def sismember(self, key, value):
        return self.client.sismember(key, value)

    def keys(self, pattern='*'):
        return list(map(redis_decode, self.client.keys(pattern)))

    def sdiff(self, keys, *args):
        return self.client.sdiff(keys, *args)

    def delete(self, *keys):
        return self.client.delete(*keys)

    def lpush(self, key, *values):
        return self.client.lpush(key, *values)

    def llen(self, key):
        return self.client.llen(key)

    def blpop(self, keys, timeout=0):
        return redis_decode(self.client.blpop(keys, timeout))[-1]

    def brpoplpush(self, src, dst, timeout=0):
        return redis_decode(self.client.brpoplpush(src, dst, timeout))

    def lpop(self, key):
        return redis_decode(self.client.lpop(key))

    def rpop(self, key):
        return redis_decode(self.client.rpop(key))

    def brpop(self, keys, timeout=0):
        return redis_decode(self.client.brpop(keys, timeout))[-1]

    def lall(self, key):
        return [redis_decode(it) for it in self.client.lrange(key, 0, -1)]

    def lrem(self, key, value):
        self.client.lrem(key, 0, value)

    def lpopall(self, key):
        items = [redis_decode(it) for it in self.client.lrange(key, 0, -1)]
        self.delete(key)
        return items

    def rpush(self, key, *values):
        return self.client.rpush(key, *values)
