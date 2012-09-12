import os
import cPickle
import thread
import copy
import urlparse
import re
from flask import Flask, send_from_directory, redirect
from base62_converter import saturate, dehydrate
from store import urls, visits, redis
app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/<uid>")
def get_url(uid):
    url = urls.get(uid)
    if url:
        visits.incr(uid)
        fullurl = 'http://' +re.sub('\s*\:\/\/','',url)
        print 'Redirecting to %s' % fullurl
        return redirect(fullurl)
    return "No such url %s !" % uid


@app.route("/shorten/<url>")
def shorten(url):
    cnt = redis.incr('count')
    uid = dehydrate(cnt)
    urls.set(uid, url)
    return "Shortened to %s" % uid


@app.route("/info/<uid>")
def info(uid):
    url = urls.get(uid)
    visit_count = visits.get(uid)
    if url and visit_count:
        return "Url: %s visited %s times" % (url, visit_count)
    return "No such url %s !" % uid

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
