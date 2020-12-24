from django.core.management.base import BaseCommand
from StreamServerApp.database_utils import delete_DB_Infos, update_db_from_local_folder
from django.conf import settings


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
        update_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL, keep_files)
