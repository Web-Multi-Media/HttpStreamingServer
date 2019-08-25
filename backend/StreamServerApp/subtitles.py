from datetime import timedelta

from babelfish import Language
from subliminal import Video, list_subtitles, region, download_best_subtitles, save_subtitles, scan_videos, scan_video

def init_cache():
    region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'}, replace_existing_backend=True)


def get_subtitles(video_path):

    # scan for videos newer than 2 weeks and their existing subtitles in a folder
    # videos = scan_videos(video_path, age=timedelta(weeks=2))
    video = Video.fromname(video_path)

    subtitles = list_subtitles([video], {Language('FR')})

    # download best subtitles
    #subtitles = download_best_subtitles(videos, {Language('eng'), Language('fra')})

    # save them to disk, next to the video
    #for v in videos:
    #    save_subtitles(v, subtitles[v])