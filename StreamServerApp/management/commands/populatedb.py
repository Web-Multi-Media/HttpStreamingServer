from django.core.management.base import BaseCommand
from os import listdir
from os.path import isfile, join
from StreamServerApp.models import Video
from django.conf import settings


class Command(BaseCommand):
    help = 'Populate video database'

    def handle(self, *args, **kwargs):
        my_path = settings.SERVER_VIDEO_DIR
        for f in listdir(my_path):
            if isfile(join(my_path, f)) and f.endswith(".mp4"):
                v = Video(name="f", baseurl=settings.REMOTE_VIDEO_DIR + "/" + f)
                v.save()
