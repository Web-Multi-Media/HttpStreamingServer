from django.core.management.base import BaseCommand
from StreamServerApp.database_utils import update_db_from_local_folder_async

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import traceback
from django.core.cache import cache
from rest_framework import permissions
from StreamServerApp.media_management.timecode import timecodeToSec


class RestUpdate(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        keep_files = False
        try:
            print(request.data["headers"]["keep_files"])
            if (request.data["headers"]["keep_files"]):
                keep_files = True
        except Exception as ex:
            keep_files = False

        is_updateing = cache.get("is_updating")
        if is_updateing is None or is_updateing == "false":
            is_updateing = cache.set("is_updating", "true", timeout=None)
            update_db_from_local_folder_async.delay(keep_files)
            cache.set("processing_state", "starting", timeout=None)
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_226_IM_USED)

    def get(self, request):
        processing_state = cache.get("processing_state")
        percentage = None
        try:
            if "video" in processing_state:
                total_nb_frame = int(cache.get("video_frames"))
                current_num_frame = 0
                for line in reversed(list(open("/usr/progress/progress-log.txt"))):
                    if "frame=" in line:
                        current_num_frame = int(line[6:])
                        break
                percentage = float(current_num_frame) / float(total_nb_frame)
                print("video percentage " + str(percentage))
            elif "audio" in processing_state:
                audio_total_duration = float(cache.get("audio_total_duration"))
                for line in reversed(list(open("/usr/progress/progress-log.txt"))):
                    if "out_time=" in line:
                        current_duration_str = line[9:]
                        current_duration = float(timecodeToSec(current_duration_str))
                        percentage = float(current_duration) / audio_total_duration
                        break
                print("audio percentage " + str(percentage))
        except:
            percentage = None


        print("processing_state state = " + processing_state)

        processing_file = cache.get("processing_file")
        data = {
            'processing_state': processing_state,
            'processing_file' : processing_file,
            'percentage': percentage,
        }
        return Response(data, status=status.HTTP_200_OK)
