import os
from flask import Flask,send_from_directory
from base62_converter import saturate, dehydrate
app = Flask(__name__)

cnt = 0
shortened_urls = []
url_visits = []

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/<uid>")
def get_url(uid):
	key = saturate(uid)
	if key < len(shortened_urls):
		url_visits[key] += 1
		return shortened_urls[key]
	return "No such url %s !" % uid

@app.route("/shorten/<url>")
def shorten(url):
	global cnt
	cnt += 1
	uid = dehydrate(cnt)
	shortened_urls.append(url)
	url_visits.append(0)
	return "Shortened to %s"%uid

@app.route("/info/<uid>")
def info(uid):
	key = saturate(uid)
	if key < len(shortened_urls):
		return "Url: %s visited %s times" %(shortened_urls[key],url_visits[key])
	return "No such url %s !" % uid

if __name__ == "__main__":
    app.run( debug=True)