import os
import urlparse

import redis

url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'))

redis = redis.StrictRedis(host=url.hostname, port=url.port, db=0, password=url.password)
