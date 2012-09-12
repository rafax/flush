import os
import urlparse

import redis

url = urlparse.urlparse(
    os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'))

redis = redis.StrictRedis(
    host=url.hostname, port=url.port, db=0, password=url.password)


class EntitySetWrapper(object):
    """docstring for Urls"""
    def __init__(self, format):
        super(EntitySetWrapper, self).__init__()
        self.format = format

    def get(self, key):
        return redis.get(self.format % key)

    def set(self, key, value):
        return redis.set(self.format % key,value)

    def incr(self, key):
        return redis.incr(self.format % key)

urls = EntitySetWrapper("u:%s")
visits = EntitySetWrapper("v:%s")