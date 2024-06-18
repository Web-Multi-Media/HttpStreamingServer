from celery import shared_task
from StreamServerApp.models import Video, Series, Movie, Subtitle
from django.conf import settings
from StreamServerApp.media_management.cover_downloader import cover_downloader

import logging

logger = logging.getLogger("root")
cvdwnld = cover_downloader()


@shared_task
def sync_subtitles(subtitle_id):
    subtitle = Subtitle.objects.get(id=subtitle_id)
    subtitle.resync()
    return 0


@shared_task
def get_subtitles_async(video_id, video_path, remote_url):
    video = Video.objects.get(id=video_id)
    try:
        video.get_subtitles(video_path, remote_url)
    except Exception as e:
        logger.exception(e)
    return 0


@shared_task
def download_cover_async(id, name, is_tv_show=False):
    output_file = "/usr/static/{}.jpeg".format(name)
    ret = cvdwnld.download_cover(name, output_file, is_tv_show)
    if ret:
        video = Video.objects.get(id=id)
        if is_tv_show:
            serie = Series.objects.get(id=video.series_id)
            serie.thumbnail = "/static/{}.jpeg".format(name)
            serie.save()
        else:
            video.thumbnail = "/static/{}.jpeg".format(name)
            video.save()

    return 0
