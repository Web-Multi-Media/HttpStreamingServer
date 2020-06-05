from django.core.management.base import BaseCommand
from StreamServerApp.database_utils import delete_DB_Infos, populate_db_from_local_folder
from django.conf import settings


class Command(BaseCommand):
    help = 'Populate video database'

    def handle(self, *args, **kwargs):
        delete_DB_Infos()
        populate_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
