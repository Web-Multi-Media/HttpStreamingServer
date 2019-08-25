from datetime import timedelta

from babelfish import Language
from subliminal import Video, subtitle, list_subtitles, region, download_best_subtitles, download_subtitles, save_subtitles, scan_videos, scan_video
import os
import subprocess
from StreamingServer.settings import customstderr, customstdout

#https://subliminal.readthedocs.io/en/latest/user/usage.html


def init_cache():
    """ # init cache for subtitles database query and stuff.
    """
    if(os.path.isfile('cachefile.dbm.db') == False):
        print("Create subtitles cache data")
        region.configure('dogpile.cache.dbm', arguments={
            'filename': 'cachefile.dbm'}, replace_existing_backend=True)


def get_subtitles(video_path):
    """ # get subtitles and convert them to web vtt
        Args:
        video_path: absolute path to videos
        return: empty string if no subtitles was found. Otherwise return subtitle absolute location
    """

    webvtt_fullpath = ''

    video = Video.fromname(video_path)

    best_subtitles = download_best_subtitles([video], {Language('fra')})

    if(best_subtitles[video]):
        best_subtitle = best_subtitles[video][0]
        value = save_subtitles(video, [best_subtitle], encoding='utf8')
        if(len(value) > 0):
            print("converting srt to vtt")
            srt_fullpath = subtitle.get_subtitle_path(
                video_path, Language('fra'))
            webvtt_fullpath = os.path.splitext(srt_fullpath)[0]+'.vtt'
            try:
                subprocess.run(
                    ["ffmpeg", "-n", "-sub_charenc", "UTF-8", "-i", srt_fullpath, webvtt_fullpath])
                return webvtt_fullpath
            except subprocess.CalledProcessError as e:
                print(e.returncode)
                print(e.cmd)
                print(e.output)
                raise
