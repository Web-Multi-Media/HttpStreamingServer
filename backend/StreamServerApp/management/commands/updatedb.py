from django.core.management.base import BaseCommand
from StreamServerApp.database_utils import delete_DB_Infos, update_db_from_local_folder
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import traceback
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Update video database'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--keepfiles',
            action='store_true',
            help='keep video files instead of deleting it in case of conversion',
        )

    def handle(self, *args, **kwargs):
        keep_files = False
        if kwargs['keepfiles']:
            keep_files = True
        is_updateing = cache.get("is_updating")
        if not is_updateing:
            update_db_from_local_folder(
                settings.VIDEO_ROOT, settings.VIDEO_URL, keep_files, async_update=True)
            update_db_from_local_folder(
                "/usr/torrent/", "/torrents/", keep_files, async_update=True)
            cache.set("is_updating", "false", timeout=None)
        else:
            print("an update is already running")