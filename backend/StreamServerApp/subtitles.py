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


def handle_subliminal_download(video, video_path):
    """ # Download the best subtitles in french and english
        Args:
        video : Name of video
        video_path: absolute path to videos
    """
    best_subtitles = download_best_subtitles([video], {Language('fra'),Language('eng')})
    if best_subtitles[video]:

        if best_subtitles[video][0].language == Language('eng') :
            best_subtitle_eng = best_subtitles[video][0]
            best_subtitle_fr = best_subtitles[video][1]
        else : 
            best_subtitle_fr = best_subtitles[video][0]
            best_subtitle_eng = best_subtitles[video][1]

        value_fr = save_subtitles(video, [best_subtitle_fr], encoding='utf8')
        value_eng = save_subtitles(video, [best_subtitle_eng], encoding='utf8')
        webvtt_fullpath=[]

        if len(value_fr) > 0:
            srt_fullpath = subtitle.get_subtitle_path(
                video_path, Language('fra'))
            webvtt_fr_fullpath = os.path.splitext(srt_fullpath)[0]+'.vtt'
            if(os.path.isfile(webvtt_fr_fullpath) is True):
                #return subtitles path even if subtitles are already downloaded/converted
                webvtt_fullpath.append(webvtt_fr_fullpath)
            if(os.path.isfile(srt_fullpath)): 
                convert_subtitles_to_webvtt(srt_fullpath, webvtt_fr_fullpath)
                webvtt_fullpath.append(webvtt_fr_fullpath)

        if len(value_eng) > 0:
            srt_fullpath = subtitle.get_subtitle_path(
                video_path, Language('eng'))
            webvtt_en_fullpath = os.path.splitext(srt_fullpath)[0]+'.vtt'
            if(os.path.isfile(webvtt_en_fullpath) is True):
                #return subtitles path even if subtitles are already downloaded/converted
                webvtt_fullpath.append(webvtt_en_fullpath)
            if(os.path.isfile(srt_fullpath)): 
                convert_subtitles_to_webvtt(srt_fullpath, webvtt_en_fullpath)
                webvtt_fullpath.append(webvtt_en_fullpath)
                
        return webvtt_fullpath
    else:
        return ''


def get_subtitles(video_path, ov_subtitles):
    """ # get subtitles and convert them to web vtt
        Args:
        video_path: absolute path to videos
        ov_subtitles: boolean (True if input has subtitles, False if not)
        return: empty string if no subtitles was found. Otherwise return subtitle absolute location
    """
    webvtt_fullpath = ''
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
        webvtt_fullpath=handle_subliminal_download(video,video_path)
    except:
        webvtt_fullpath = ''

    if webvtt_fullpath != '' :
        webvtt_fr_fullpath = webvtt_fullpath[0]
        webvtt_en_fullpath = webvtt_fullpath[1]

    return (webvtt_fr_fullpath, webvtt_en_fullpath, webvtt_ov_fullpath)