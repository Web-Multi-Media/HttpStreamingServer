from celery import shared_task
from StreamServerApp.media_processing import convert_subtitles_to_webvtt
from StreamServerApp.database_utils import update_db_from_local_folder
import subprocess

@shared_task
def sync_subtitles(video_path,subtitle_path, synchronized_subtitle_path):
    print(" ".join(["ffs",video_path,"-i",subtitle_path,"-o",synchronized_subtitle_path]))
    subprocess.run(["ffs",video_path,"-i",subtitle_path,"-o",synchronized_subtitle_path])
    print('sucess')
    # ffs video_path -i subtitle_path -o synchronized_subtitle_path
@shared_task
def convert_subtitles(input_path,output_path):
    convert_subtitles_to_webvtt(input_path,output_path)
    print(output_path)

@shared_task
def update_db_after_sync(base_path,remote_url):
    update_db_from_local_folder(base_path, remote_url)