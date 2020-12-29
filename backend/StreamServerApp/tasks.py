from celery import shared_task
from StreamServerApp.models import Video, Series, Movie, Subtitle
import subprocess
import os
from django.conf import settings


@shared_task
def sync_subtitles(video_id, subtitle_id):
    video = Video.objects.get(id=video_id)
    video.sync_subtitles(subtitle_id)
    return 0


@shared_task
def get_subtitles_async(video_id, ov_subtitles):
    video = Video.objects.get(id=video_id)
    video.get_subtitles(ov_subtitles)
    return 0
