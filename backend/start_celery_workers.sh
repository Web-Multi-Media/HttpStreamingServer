mkdir -p $HOME/run/celery/
mkdir -p $HOME/log/celery/ 
touch "$HOME/log/celery/test.log"
rm "$HOME/run/celery/*.pid"
celery multi start 2 -A StreamingServer  -B:2 -Q:2 cpu_extensive -c:2 1 --pidfile="$HOME/run/celery/%n.pid" --logfile="$HOME/log/celery/test.log"
tail -f "$HOME/log/celery/test.log"