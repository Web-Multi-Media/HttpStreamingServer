from django.core.management.base import BaseCommand
import os
from os.path import isfile, join
from StreamServerApp.models import Video
from django.conf import settings


VIDEO_NAMES = ['canard', 'cochon', 'singe']


class Command(BaseCommand):
    help = 'Populate video database'

    def handle(self, *args, **kwargs):
        Video.objects.all().delete()  # delete all videos in the db
        my_path = settings.SERVER_VIDEO_DIR
        idx = 0
        for root, directories, filenames in os.walk(my_path):
            idx += len(filenames)
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, my_path)
                if isfile(full_path) and full_path.endswith(".mp4"):
                    v = Video(
                        name=VIDEO_NAMES[idx % 3], baseurl=settings.REMOTE_BASE_URL + "/" + relative_path)
                    v.save()
