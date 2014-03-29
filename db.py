import os
import urlparse

import redis

def FlushDb():

	def __init__(self):
		pass

	redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'))

	r = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port, db=0, password=redis_url.password)

db = FlushDb()


