import os
from babelfish import Language
from subliminal import Video, subtitle, region, download_best_subtitles, save_subtitles

from StreamServerApp.media_processing import extract_subtitle, convert_subtitles_to_webvtt

#https://subliminal.readthedocs.io/en/latest/user/usage.html


def init_cache():
    """ # init cache for subtitles database query and stuff.
    """
    if(os.path.isfile('cachefile.dbm.db') == False):
        print("Create subtitles cache data")
        region.configure('dogpile.cache.dbm', arguments={
            'filename': 'cachefile.dbm'}, replace_existing_backend=True)


def handle_subliminal_download(video, video_path, langage):
    best_subtitles = download_best_subtitles([video], {Language(langage)})
    if best_subtitles[video]:
        best_subtitle = best_subtitles[video][0]
        value = save_subtitles(video, [best_subtitle], encoding='utf8')
        if len(value) > 0:
            srt_fullpath = subtitle.get_subtitle_path(
                video_path, Language(langage))
            webvtt_en_fullpath = os.path.splitext(srt_fullpath)[0]+'.vtt'
            if(os.path.isfile(webvtt_en_fullpath) == True):
                #return subtitles path even if subtitles are already downloaded/converted
                return webvtt_en_fullpath
            if(os.path.isfile(srt_fullpath)): 
                convert_subtitles_to_webvtt(srt_fullpath, webvtt_en_fullpath)
                return webvtt_en_fullpath
    else:
        return ''


def get_subtitles(video_path, ov_subtitles):
    """ # get subtitles and convert them to web vtt
        Args:
        video_path: absolute path to videos
        ov_subtitles: boolean (True if input has subtitles, False if not)
        return: empty string if no subtitles was found. Otherwise return subtitle absolute location
    """

    webvtt_fr_fullpath = ''
    webvtt_en_fullpath = ''
    webvtt_ov_fullpath = ''

    if ov_subtitles:
        try:
            webvtt_ov_fullpath = os.path.splitext(video_path)[0]+'_ov.vtt'
            extract_subtitle(video_path, webvtt_ov_fullpath)
        except:
            webvtt_ov_fullpath = ''

    video = Video.fromname(video_path)

    try:
        webvtt_en_fullpath = handle_subliminal_download(video, video_path, 'eng')
    except:
        webvtt_en_fullpath = ''
    
    try:
        webvtt_fr_fullpath = handle_subliminal_download(video, video_path, 'fra')
    except:
        webvtt_fr_fullpath = ''

    return (webvtt_fr_fullpath, webvtt_en_fullpath, webvtt_ov_fullpath)
