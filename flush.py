import os
import cPickle
import thread
import copy
import urlparse
import json
import re
import datetime
from flask import Flask, send_from_directory, redirect, request, render_template,url_for
from base62_converter import saturate, dehydrate
from store import urls, visits, redis
app = Flask(__name__)


@app.route("/<uid>")
def get_url(uid):
    url = urls.get(uid)
    if url:
        cnt = visits.incr(uid)
        redis.set("v:%s:%s" % (uid, cnt),
            json.dumps({
                'values': request.values,
                'headers': list(request.headers),
                'url': request.url,
                'method': request.method,
                'date': datetime.datetime.now().isoformat(),
                'ip': request.remote_addr
                },
                sort_keys=True, indent=4))
        fullurl = to_full(url)
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
    if url:
        visit_count = visits.get(uid)
        ret = "Url: %s visited %s times" % (url, visit_count)
        ret += "<br />"
        visit_keys = redis.keys("v:%s:*" % uid)
        ret += "<br />".join(map(lambda k: json.dumps(json.loads(redis.get(k)), sort_keys=True, indent=4), visit_keys))
        return ret
    return "No such url %s !" % uid


@app.route("/secret")
def secret():
    url_keys = sorted(redis.keys('url:*'))
    links = map(lambda u: "%(key)s => <a href='%(url)s'> %(url)s</a> <a href='%(info_url)s'>Info</a>" %
                            {'key': u, 'url': to_full(redis.get(u)), 'info_url': url_for('info',uid=u.replace("url:",""))},url_keys)
    return '<br />'.join(links)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def favicon():
    return 'Welcome to flush, FLask based Url SHortener!'


@app.route('/mu-ec2f18e2-3a51503c-b31d1c19-e0f57a1a')
def blitz():
    return '42'


def to_full(url):
    return 'http://' + re.sub('\s*\:\/\/', '', url)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
