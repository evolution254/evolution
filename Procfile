web: gunicorn newrevolution.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A newrevolution worker --loglevel=info
beat: celery -A newrevolution beat --loglevel=info