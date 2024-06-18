service transmission-daemon start
python3 /usr/src/app/manage.py collectstatic --no-input 
python3 /usr/src/app/manage.py clearcache
if [[ "$DEPLOY_ENV" == "development" ]]
then
    ./wait-for-it.sh db:5432 -- python3 /usr/src/app/manage.py runserver 0.0.0.0:8000
else
    gunicorn --workers=${NUM_GUNICORN_WORKER} StreamingServer.wsgi:application --bind 0.0.0.0:8000
fi
