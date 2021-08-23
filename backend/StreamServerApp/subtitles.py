import os
from babelfish import Language
from subliminal import Video, subtitle, region, download_best_subtitles, save_subtitles
import io

from StreamServerApp.media_processing import extract_subtitle, convert_subtitles_to_webvtt

#https://subliminal.readthedocs.io/en/latest/user/usage.html


def init_cache():
    """ # init cache for subtitles database query and stuff.
    """
    if not os.path.isfile('cachefile.dbm.db'):
        print("Create subtitles cache data")
        region.configure('dogpile.cache.dbm', arguments={
            'filename': 'cachefile.dbm'}, replace_existing_backend=True)


def remove_nullcharacters(fname):
    flist = open(fname).readlines()
    output = []
    for s in flist:
        output.append(s.replace('\0', ''))
    return output


def handle_subliminal_download(video, video_path, languages_to_retrieve):
    """ # Download the best subtitles in french and english
        Args:
        video : Name of video
        video_path: absolute path to videos
        languages_to_retrieve : dict of subtitles languages to retrieve
        return : two dicts with the path of each subtitles with str of language as key / Exemple : 'eng' for english, 'fra' for french .
        the first dict is the path to vtt subtitles, the second one is the path to str subtitles
    """

    webvtt_subtitles_returned = {}
    srt_subtitles_returned = {}
    best_subtitles = download_best_subtitles(
        [video], set(map(Language, languages_to_retrieve)))
    if best_subtitles[video]:
        for retrieved_subtitle in best_subtitles[video]:
            subtitles_are_saved = save_subtitles(
                video, [retrieved_subtitle], encoding='utf8')
            if subtitles_are_saved:
                srt_fullpath = subtitle.get_subtitle_path(
                    video_path, retrieved_subtitle.language)
                srt_subtitles_returned[
                    retrieved_subtitle.language.alpha3] = srt_fullpath
                new_data = remove_nullcharacters(srt_fullpath)
                with io.open(srt_fullpath, 'w', encoding='utf-8') as f:
                    for line in new_data:
                        f.write(line)
                webvtt_fullpath = os.path.splitext(srt_fullpath)[0]+'.vtt'
                if os.path.isfile(webvtt_fullpath):
                    # Add the subtitles path to subtitles_returned even if they are already downloaded/converted
                    webvtt_subtitles_returned[
                        retrieved_subtitle.language.alpha3] = webvtt_fullpath
                if os.path.isfile(srt_fullpath):
                    # Add the subtitles path to subtitles_returned after converting them in .vtt
                    convert_subtitles_to_webvtt(srt_fullpath, webvtt_fullpath)
                    webvtt_subtitles_returned[
                        retrieved_subtitle.language.alpha3] = webvtt_fullpath
    return webvtt_subtitles_returned, srt_subtitles_returned


def get_subtitles(video_path):
    """ # get subtitles and convert them to web vtt
        Args:
        video_path: absolute path to videos
        return: empty string if no subtitles was found. Otherwise return dict of subtitle absolute location with str(Language) as key
    """
    languages_to_retrieve = {
        'eng',
        'fra',
    }
    webvtt_fullpath = {}
    srt_fullpath = {}

    try:
        video = Video.fromname(video_path)
        try:
            webvtt_fullpath, srt_fullpath = handle_subliminal_download(
                video, video_path, languages_to_retrieve)
        except:
            webvtt_fullpath = {}
            srt_fullpath = {}
    except ValueError:
        #This usually happens when there is not enough data for subliminal to guess
        pass

    return [webvtt_fullpath, srt_fullpath]
