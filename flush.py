import os
import json
import re
import datetime
from flask import Flask, send_from_directory, redirect, request, render_template, url_for, flash, abort
from base62_converter import dehydrate
from store import urls, visits, stats
app = Flask(__name__)
app.secret_key = os.environ.get(
    'APP_SECRET', '\x08/\x176\xcb\x8b\x0f\xa4g\x0b\xff\xb3{\xefP\xd6\x85>\x97\xf4X\xce\xcb\xc1')


@app.route("/<uid>")
def redirect_to_url(uid):
    url = get_url(uid)
    if not url:
        return abort(404)
    return redirect(url)


@app.route("/benchmark/<uid>")
def return_url(uid):
    found, url = get_url(uid)
    if not found:
        return abort(404)
    return url

def get_url(uid):
    url = urls.get(uid)
    if not url:
        return None
    cnt = visits.incr(uid)
    stats.incr('visits')
    visits.set("%s:%s" % (uid, cnt),
               json.dumps({
                          'values': request.values,
                          'headers': list(request.headers),
                          'url': request.url,
                          'method': request.method,
                          'date': datetime.datetime.now().isoformat(),
                          'ip': request.remote_addr
                          }))
    fullurl = to_full(url)
    return fullurl

@app.route("/shorten", methods=['POST'])
def shorten():
    proposed_name = request.form['proposed_name']
    url = request.form['url']
    if proposed_name:
        if not urls.setnx(proposed_name, 'PLACEHOLDER'):
            flash('Cannot shorten to %s' % proposed_name)
            return render_template('home.html', url=url, proposed_name=proposed_name)
        uid = proposed_name
        stats.incr('count')
    else:
        uid = dehydrate(stats.incr('count'))
    urls.set(uid, url)
    flash("Shortened to %s" % uid)
    return redirect(url_for('info', uid=uid))


@app.route("/info/<uid>")
def info(uid):
    url = urls.get(uid)
    if url:
        visit_count = visits.get(uid)
        visit_keys = visits.keys("%s:*" % uid)
        values = visits.fetch_all(visit_keys)
        return render_template('info.html', url=url, full_url=to_full(url), visit_count=visit_count, visits=values)
    return "No such url %s !" % uid


@app.route("/secret")
def secret():
    url_keys = urls.keys()
    all_urls = urls.fetch_all(url_keys)
    full_urls = []
    for u, url in zip(url_keys, all_urls):
        full_urls.append({'key': u, 'url': url, 'full_url': to_full(url), 'uid': u.replace(
            "url:", ""), 'info_url': url_for('info', uid=u.replace("url:", ""))})
    return render_template('secret.html', urls=full_urls)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/mu-ec2f18e2-3a51503c-b31d1c19-e0f57a1a')
def blitz():
    return '42'


def to_full(url):
    return 'http://' + re.sub('^\w*\:\/\/', '', url)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
