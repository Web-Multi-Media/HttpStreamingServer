import os
from babelfish import Language
from subliminal import Video, subtitle, region, download_best_subtitles, save_subtitles

from StreamServerApp.media_processing import extract_subtitle, convert_subtitles_to_webvtt

#https://subliminal.readthedocs.io/en/latest/user/usage.html


def init_cache():
    """ # init cache for subtitles database query and stuff.
    """
    if not os.path.isfile('cachefile.dbm.db'):
        print("Create subtitles cache data")
        region.configure('dogpile.cache.dbm', arguments={
            'filename': 'cachefile.dbm'}, replace_existing_backend=True)


def handle_subliminal_download(video, video_path, languages_to_retrieve):
    """ # Download the best subtitles in french and english
        Args:
        video : Name of video
        video_path: absolute path to videos
    """

    subtitles_returned = {}
    for language in languages_to_retrieve:
        subtitles_returned[language] = ''

    best_subtitles = download_best_subtitles([video], languages_to_retrieve)
    if best_subtitles[video]:
        for retrieved_subtitle in best_subtitles[video]:
            subtitles_are_saved = save_subtitles(
                video, [retrieved_subtitle], encoding='utf8')
            if subtitles_are_saved:
                srt_fullpath = subtitle.get_subtitle_path(
                    video_path, retrieved_subtitle.language)
                webvtt_fullpath = os.path.splitext(srt_fullpath)[0]+'.vtt'
                if(os.path.isfile(webvtt_fullpath)):
                    #Add the subtitles path to subtitles_returned even if they are already downloaded/converted
                    subtitles_returned[retrieved_subtitle.language] = webvtt_fullpath
                if(os.path.isfile(srt_fullpath)):
                    #Add the subtitles path to subtitles_returned after converting them in .vtt
                    convert_subtitles_to_webvtt(srt_fullpath, webvtt_fullpath)
                    subtitles_returned[retrieved_subtitle.language] = webvtt_fullpath
        return subtitles_returned
    else:
        return ''


def get_subtitles(video_path, ov_subtitles):
    """ # get subtitles and convert them to web vtt
        Args:
        video_path: absolute path to videos
        ov_subtitles: boolean (True if input has subtitles, False if not)
        return: empty string if no subtitles was found. Otherwise return subtitle absolute location
    """
    languages_to_retrieve = {
        Language('eng'),
        Language('fra'),
    }
    webvtt_fullpath = ''
    webvtt_ov_fullpath = ''

    if ov_subtitles:
        try:
            webvtt_ov_fullpath = os.path.splitext(video_path)[0]+'_ov.vtt'
            extract_subtitle(video_path, webvtt_ov_fullpath)
        except:
            webvtt_ov_fullpath = ''

    video = Video.fromname(video_path)

    try:
        webvtt_fullpath = handle_subliminal_download(
            video, video_path, languages_to_retrieve)
    except:
        webvtt_fullpath = ''

    ### to Enhance For more languages -> Change in the return and dependancies
    if webvtt_fullpath != '':
        webvtt_fr_fullpath = webvtt_fullpath[Language('fra')]
        webvtt_en_fullpath = webvtt_fullpath[Language('eng')]

    return (webvtt_fr_fullpath, webvtt_en_fullpath, webvtt_ov_fullpath)
