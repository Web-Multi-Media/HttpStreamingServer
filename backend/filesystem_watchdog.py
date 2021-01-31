import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from StreamServerApp.models import Video, Series, Movie, Subtitle

def on_created(event):
    print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = "/usr/src/app/Videos"
    event_handler = LoggingEventHandler()
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()