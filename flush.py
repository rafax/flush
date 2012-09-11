import os
import pickle
from flask import Flask,send_from_directory
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
		pickle.dump(url_visits,open('url_visits.db','w'))
		return shortened_urls[uid]
	return "No such url %s !" % uid

@app.route("/shorten/<url>")
def shorten(url):
	global cnt
	cnt += 1
	uid = dehydrate(cnt)
	shortened_urls[uid]=url
	url_visits[uid]=0
	pickle.dump(shortened_urls,open('shortened_urls.db','w'))
	pickle.dump(url_visits,open('url_visits.db','w'))
	return "Shortened to %s"%uid

@app.route("/info/<uid>")
def info(uid):
	if uid in shortened_urls:
		return "Url: %s visited %s times" %(shortened_urls[uid],url_visits[uid])
	return "No such url %s !" % uid

if __name__ == "__main__":
	if os.path.exists('shortened_urls.db'):
		shortened_urls = pickle.load(open('shortened_urls.db','r'))
		cnt = len(shortened_urls)
	if os.path.exists('url_visits.db'):
		url_visits = pickle.load(open('url_visits.db','r'))
	app.run( debug=True)
