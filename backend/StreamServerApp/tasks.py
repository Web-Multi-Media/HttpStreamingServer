from celery import shared_task
from StreamServerApp.models import Video, Series, Movie, Subtitle
from StreamServerApp.media_processing import convert_subtitles_to_webvtt
from StreamServerApp.subtitles import get_subtitles
import subprocess
import os
from django.conf import settings



@shared_task
def sync_subtitles( video_id, subtitle_id):
    video = Video.objects.get(id=video_id)
    video_path = os.path.join(settings.VIDEO_ROOT, video.video_url.split(settings.VIDEO_URL)[1])
    assert(os.path.isfile(video_path))
    subtitle = Subtitle.objects.get(id=subtitle_id)
    subtitle_path = subtitle.srt_path
    assert(os.path.isfile(subtitle_path))
    webvtt_path = subtitle.vtt_path.replace('.vtt', '_sync.vtt')
    #print(webvtt_path)
    sync_subtitle_path = subtitle_path.replace('.srt', '_sync.srt')
    subprocess.run(["ffs", video_path, "-i", subtitle_path, "-o", sync_subtitle_path])
    convert_subtitles_to_webvtt(sync_subtitle_path, webvtt_path)
    subtitle.srt_sync_path = sync_subtitle_path
    subtitle.vtt_sync_path = webvtt_path
    subtitle.webvtt_sync_url = os.path.join(settings.VIDEO_URL, webvtt_path.split(settings.VIDEO_ROOT)[1])
    subtitle.save()

@shared_task
def get_subtitles_async(video_id, ov_subtitles):
    video = Video.objects.get(id=video_id)
    video_path = os.path.join(settings.VIDEO_ROOT, video.video_url.split(settings.VIDEO_URL)[1])
    subtitles_list = get_subtitles(video_path, ov_subtitles)

    webvtt_subtitles_full_path = subtitles_list[0]
    srt_subtitles_full_path = subtitles_list[1]
    webvtt_subtitles_remote_path = {}
    for language_str, srt_subtitle_url in webvtt_subtitles_full_path.items():
        webvtt_subtitles_remote_path[language_str] = ''
        vtt_subtitle_url = webvtt_subtitles_full_path[language_str]
        if srt_subtitle_url and vtt_subtitle_url:
            webvtt_subtitles_relative_path = os.path.relpath(
                vtt_subtitle_url, video_path)
            newsub = Subtitle()
            newsub.video_id = video.id
            newsub.vtt_path = vtt_subtitle_url
            if srt_subtitles_full_path.get(language_str):
                newsub.srt_path = srt_subtitles_full_path[language_str]
            newsub.webvtt_subtitle_url = os.path.join(
                settings.VIDEO_URL, webvtt_subtitles_relative_path)
            newsub.language = language_str
            newsub.save()
    return 0
