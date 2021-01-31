import watchdog.events
from StreamServerApp.database_utils import add_one_video_to_database
from StreamServerApp.models import Video, Series, Movie, Subtitle
from StreamingServer.settings import VIDEO_ROOT, VIDEO_URL
import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.mp4', '*.mkv'],
                                                             )

    def on_created(self, event):
        num_results = Video.objects.filter(video_folder=event.src_path).count()
        if (num_results == 0):
            relative_path = os.path.relpath(VIDEO_ROOT, event.src_path)
            filename = os.path.basename(event.src_path)
            add_one_video_to_database(event.src_path, VIDEO_ROOT, relative_path, VIDEO_URL, filename)

    def on_deleted(self, event):
        print("Removing {} from db ".format(event.src_path))
        Video.objects.filter(video_folder=event.src_path).delete()
        #Remove empty Series/Movies dataset
        Series.objects.filter(video=None).delete()
        Movie.objects.filter(video=None).delete()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = VIDEO_ROOT
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
