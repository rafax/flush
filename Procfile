web: newrelic-admin run-program gunicorn flush:app -b 0.0.0.0:$PORT -w 4
worker: celery -A flush:celery worker