from os import path, environ
import datetime
import re
from flask import Flask, send_from_directory, \
    redirect, request, render_template, url_for, flash, abort
from db import db
app = Flask(__name__)
app.secret_key = environ.get(
    'APP_SECRET',
    '''\x08/\x176\xcb\x8b\x0f\xa4g\x0b
    \xff\xb3{\xefP\xd6\x85>\x97\xf4X\xce\xcb\xc1''')


@app.route("/<uid>")
def redirect_to_url(uid):
    full_url = url_visited(uid)
    return redirect(full_url)


@app.route("/benchmark/<uid>")
def return_url(uid):
    full_url = url_visited(uid)
    return full_url


def url_visited(uid):
    visit_data = {
        'values': request.values,
        'headers': list(request.headers),
        'url': request.url,
        'method': request.method,
        'date': datetime.datetime.now().isoformat(),
        'ip': request.remote_addr
    }
    url = db.url_visited(uid, visit_data)
    if not url:
        return abort(404)
    return to_full(url)


@app.route("/shorten", methods=['POST'])
def shorten():
    proposed_name = request.form['proposed_name']
    url = request.form['url']
    uid = db.shorten_url(url, proposed_name)
    if not uid:
        flash('Cannot shorten to %s' % proposed_name)
        return render_template('home.html', url=url,
                               proposed_name=proposed_name)
    flash("Shortened to %s" % uid)
    return redirect(url_for('info', uid=uid))


@app.route("/info/<uid>")
def info(uid):
    url = db.get_url(uid)
    if url:
        visits = db.url_visits(uid)
        return render_template('info.html', url=url, full_url=to_full(url),
                               visit_count=len(visits), visits=visits)
    return "No such url %s !" % uid


@app.route("/secret")
def secret():
    all_urls = db.all_urls()
    full_urls = []
    for uid, url in all_urls.items():
        full_urls.append(
            {'url': url, 'full_url': to_full(url),
             'uid': uid, 'info_url': url_for('info', uid=uid)})
    return render_template('secret.html', urls=full_urls)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        path.join(app.root_path, 'static'),
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
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
