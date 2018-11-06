from django.core.management.base import BaseCommand
from os import listdir
from os.path import isfile, join
from StreamServerApp.models import Video
from django.conf import settings


VIDEO_NAMES = ['canard', 'cochon', 'singe']

class Command(BaseCommand):
    help = 'Populate video database'

    def handle(self, *args, **kwargs):
        Video.objects.all().delete()  # delete all videos in the db
        my_path = settings.SERVER_VIDEO_DIR
        for idx, f in enumerate(listdir(my_path)):
            if isfile(join(my_path, f)) and f.endswith(".mp4"):
                v = Video(name=VIDEO_NAMES[idx % 3], baseurl=settings.REMOTE_BASE_URL + "/" + f)
                v.save()
