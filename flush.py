import os
import cPickle
import thread
import copy
from flask import Flask, send_from_directory
from base62_converter import saturate, dehydrate
from store import redis
app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/<uid>")
def get_url(uid):
    url = redis.get('u:%s' % uid)
    if url:
        redis.incr('v:%s' % uid)
        return url
    return "No such url %s !" % uid


@app.route("/shorten/<url>")
def shorten(url):
    cnt = redis.incr('count')
    uid = dehydrate(cnt)
    redis.set('u:%s' % uid, url)
    return "Shortened to %s" % uid


@app.route("/info/<uid>")
def info(uid):
    url = redis.get('u:%s' % uid)
    visits = redis.get('v:%s' % uid)
    if url and visits:
        return "Url: %s visited %s times" % (url, visits)
    return "No such url %s !" % uid

if __name__ == "__main__":
    app.run(debug=True)
