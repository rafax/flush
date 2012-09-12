import os
import urlparse

import redis

_url = urlparse.urlparse(
    os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'))



class _EntitySetWrapper(object):
    """docstring for Urls"""
    def __init__(self, format):
        super(_EntitySetWrapper, self).__init__()
        self.format = format

    def get(self, key):
        return redis.get(self.format % key)

    def set(self, key, value):
        return redis.set(self.format % key,value)

    def incr(self, key):
        return redis.incr(self.format % key)

redis = redis.StrictRedis(
    host=_url.hostname, port=_url.port, db=0, password=_url.password)
urls = _EntitySetWrapper("u:%s")
visits = _EntitySetWrapper("v:%s")