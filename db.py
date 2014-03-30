import os
import urlparse
import json

import redis

from base62_converter import dehydrate


class FlushDb():

    urls = "u:%s"
    visits = "v:%s"

    url_count = "stats:url_count"
    visit_count = "stats:visit_count"

    redis_url = urlparse.urlparse(
        os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'))

    r = redis.StrictRedis(
        host=redis_url.hostname,
        port=redis_url.port,
        db=0,
        password=redis_url.password)

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

    def url_visited(self, uid, visit_data):
        url = self.r.get(self.urls % uid)
        if not url:
            return None
        self.r.rpush(self.visits % uid, json.dumps(visit_data))
        self.r.incr(self.visit_count)
        return url

    def get_url(self, uid):
        return self.r.get(self.urls % uid)

    def url_visits(self, uid):
        return self.r.lrange(self.visits % uid, 0, -1)

    def all_urls(self):
        url_keys = self.r.keys(self.urls % '*')
        url_values = self.__fetch_all(url_keys)
        urls = {}
        for key, value in zip(url_keys, url_values):
            urls[key.replace("u:", "")] = value
        return urls

    def __fetch_all(self, keys):
        pipe = self.r.pipeline()
        for k in keys:
            pipe.get(k)
        return pipe.execute()


db = FlushDb()
