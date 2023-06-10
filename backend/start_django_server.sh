service transmission-daemon start
python3 /usr/src/app/manage.py collectstatic --no-input 
python3 /usr/src/app/manage.py clearcache
gunicorn --workers=${NUM_GUNICORN_WORKER} StreamingServer.wsgi:application --bind 0.0.0.0:8000
