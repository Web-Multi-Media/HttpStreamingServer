mkdir -p $HOME/run/celery/
mkdir -p /debug/celery/
rm "$HOME/run/celery/*.pid"
celery multi start 2 -A StreamingServer  -B:2 -Q:2 cpu_extensive -c:2 1 --pidfile="$HOME/run/celery/%n.pid" --logfile="/debug/celery/celery.log"
sleep infinity