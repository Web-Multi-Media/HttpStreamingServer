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
        update_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL, keep_files)
        update_db_from_local_folder("/usr/torrent/", "/torrents/", keep_files)


class RestUpdate(APIView):
    def post(self, request):
        try:
            user = request.api_user
            #return self.get_history(request, user)
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        is_updateing = cache.get("is_updating")
        if is_updateing is None or is_updateing == "false":
            is_updateing = cache.set("is_updating", "true")
            update_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
            update_db_from_local_folder("/usr/torrent/", "/torrents/")
            cache.set("is_updating", "false")
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_226_IM_USED)
   
