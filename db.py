import os
import urlparse

import redis

from base62_converter import dehydrate


class FlushDb():

    urls = "url:%s"
    url_count = "stats:url_count"
    visits = "url:%s:v"

    redis_url = urlparse.urlparse(
        os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'))

    r = redis.StrictRedis(
        host=redis_url.hostname, port=redis_url.port, db=0, password=redis_url.password)

    def shorten_url(self, url, proposed_name):
        if proposed_name:
            if not self.r.setnx(self.urls % proposed_name, 'PLACEHOLDER'):
                return None
            uid = proposed_name
            self.r.incr(self.url_count)
        else:
            uid = dehydrate(self.r.incr(self.url_count))
        self.r.set(self.urls % uid, url)
        return uid


db = FlushDb()
