import os
import cPickle
import thread
import copy
from flask import Flask, send_from_directory
from base62_converter import saturate, dehydrate
app = Flask(__name__)

cnt = 0
shortened_urls = {}
url_visits = {}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/<uid>")
def get_url(uid):
    if uid in shortened_urls:
        url_visits[uid] += 1
        return shortened_urls[uid]
    return "No such url %s !" % uid


@app.route("/shorten/<url>")
def shorten(url):
    global cnt
    cnt += 1
    uid = dehydrate(cnt)
    if cnt % 100 == 0:
        thread.start_new_thread(dump_to_disk, ())
    shortened_urls[uid] = url
    url_visits[uid] = 0
    return "Shortened to %s" % uid


@app.route("/info/<uid>")
def info(uid):
    if uid in shortened_urls:
        return "Url: %s visited %s times" % (shortened_urls[uid], url_visits[uid])
    return "No such url %s !" % uid

def dump_to_disk():
    print "Dumping"
    _shortened_urls = copy.copy(shortened_urls)
    _url_visits = copy.copy(url_visits)
    cPickle.dump(_shortened_urls, open('shortened_urls.db', 'w'))
    cPickle.dump(_url_visits, open('url_visits.db', 'w'))

if __name__ == "__main__":
    if os.path.exists('shortened_urls.db'):
        shortened_urls = cPickle.load(open('shortened_urls.db', 'r'))
        cnt = len(shortened_urls)
    if os.path.exists('url_visits.db'):
        url_visits = cPickle.load(open('url_visits.db', 'r'))
    app.run(debug=True)
