from celery import shared_task
from StreamServerApp.models import Video, Series, Movie
from StreamServerApp.media_processing import convert_subtitles_to_webvtt
from StreamServerApp.database_utils import update_db_from_local_folder
import subprocess

@shared_task
def sync_subtitles(language,video_path,video_id,subtitle_path, synchronized_subtitle_path,webvtt_path):
    video = Video.objects.get(id=video_id)
    subprocess.run(["ffs",video_path,"-i",subtitle_path,"-o",synchronized_subtitle_path])
    convert_subtitles_to_webvtt(synchronized_subtitle_path,webvtt_path)
    url = video.video_url.replace(video.name,'')
    synchronized_subtitle_path = synchronized_subtitle_path.replace(video.video_folder,url)
    webvtt_path = webvtt_path.replace(video.video_folder, url)
    if (language == 'en') :
        video.en_srt_sync_url = synchronized_subtitle_path
        video.en_webvtt_sync_url = webvtt_path
    if (language == 'fr') :
        video.fr_srt_sync_url = synchronized_subtitle_path
        video.fr_webvtt_sync_url = webvtt_path
    video.save()
