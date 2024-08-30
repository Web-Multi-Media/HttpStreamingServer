import os
import subprocess
import json

import re
import subliminal
import sys
import string
from django.core.cache import cache
from StreamServerApp.media_management.encoder import h264_encoder, aac_encoder, extract_audio, extract_video
from StreamServerApp.media_management.dash_packager import dash_packager
from StreamServerApp.media_management.frame_analyzer import keyframe_analysis
from StreamServerApp.media_management.media_analyzer import get_media_file_info, get_video_stream_info, get_audio_stream_info
from StreamServerApp.media_management.fileinfo import createfileinfo, readfileinfo
from StreamServerApp.media_management.subprocess_wrapper import run_subprocess
from StreamServerApp.media_management.timecode import timecodeToSec
import math

import logging 

logger = logging.getLogger("root")

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def convert_subtitles_to_webvtt(input_file, output_file):
    """ # Uses ffmpeg subprocess to convert subtitles to webvtt
    
    Args:
    input_file: full path to the input subtitle (eg: /Videos/folder1/sub.srt)
    output_file: full path to the output webvtt file (eg: /Videos/folder1/sub.vtt)

    Returns: void

    Throw an exception if the return value of the subprocess is different than 0

    """
    cmd = ["ffmpeg", "-n", "-sub_charenc", "UTF-8", "-i", input_file, output_file]
    if not os.path.isfile(output_file):
        run_subprocess(cmd)


def extract_subtitle(input_file, output_file, subtitle_index = 0):
    """ # Uses ffmpeg subprocess to extract subtitles from a video and convert it to webvtt
    
    Args:
    input_file: full path to the input video (eg: /Videos/folder1/video.mp4)
    output_file: full path to the output webvtt file (eg: /Videos/folder1/sub.vtt)
    subtitle_index: subtitle track index to extract

    Returns: void

    Throw an exception if the return value of the subprocess is different than 0

    """
    cmd = ["ffmpeg", "-n", "-sub_charenc", "UTF-8", "-i", input_file, "-map", "0:s:{}".format(subtitle_index), output_file]
    if not os.path.isfile(output_file):
        run_subprocess(cmd)


def transmux_to_mp4(input_file, output_file, with_audio_reencode=False):
    """ # Uses ffmpeg subprocess to transmux to mp4
    
    Args:
    input_file: full path to the input video (eg: /Videos/folder1/video.mp4)
    output_file: full path to the output video (eg: /Videos/folder1/video.mp4)

    Returns: void

    Throw an exception if the return value of the subprocess is different than 0

    """
    if with_audio_reencode:
        logger.debug(
            "Audio codec is not aac, audio reencoding is necessary (This might take a long time)")
        cmd = ["ffmpeg", "-i", input_file,
                "-acodec", "aac", "-vcodec", "copy", "-movflags", "+faststart", output_file]
    else:
        cmd = ["ffmpeg", "-i", input_file,
                "-codec", "copy", "-movflags", "+faststart", output_file]

    if not os.path.isfile(output_file):
        run_subprocess(cmd)


def generate_thumbnail(input_file, duration, output_file):
    """ # Uses ffmpeg subprocess to extract a thumbnail from a video
    
    Args:
    input_file: full path to the input video (eg: /Videos/folder1/video.mp4)
    duration: Video duration (in seconds). The thumbnail is taken at half the movies duration
     (to avoid black screen at the beginning or the end).
    output_file: full path to the output thumbnail file (eg: /Videos/folder1/thumb.jpeg)

    Returns: void

    Throw an exception if the return value of the subprocess is different than 0

    """
    cmd = ["ffmpeg", "-ss", str(duration/2.0), "-i", input_file, "-an", "-vf", "scale=320:-1",
                            "-vframes", "1", output_file]
    if not os.path.isfile(output_file):
        run_subprocess(cmd)


def resync_subtitle(video_path, subtitle_path, sync_subtitle_path):
    """ # Uses ffs to resync sub
    
    Args:

    Returns: void

    Throw an exception if the return value of the subprocess is different than 0

    """
    cmd = ["ffs", video_path, "-i", subtitle_path, "-o", sync_subtitle_path]
    if not os.path.isfile(sync_subtitle_path):
        run_subprocess(cmd)


def prepare_video(video_full_path,
                  video_path,
                  video_dir,
                  remote_url,
                  keep_files=False):
    """ # Create thumbnail, transmux if necessayr and get all the videos infos.
        Args:
        full_path: full path to the video (eg: /Videos/folder1/video.mp4)
        video_path: path to the video basedir (eg: /Videos/)
        video_dir: path to the video dir (eg: /Videos/folder1/)
        keep_files: Keep original files in case of convertion

        return: Dictionnary with video infos
    """
    cache.set("ingestion_task_{}".format(video_full_path), "Analyzing input", timeout=None)
    cache.set("processing_file", "{}".format(video_full_path), timeout=None)
    probe = get_media_file_info(video_full_path)

    video_tracks = []
    audio_tracks = []

    webvtt_ov_fullpaths = []
    subtitles_stream = None
    subtitles_index = 0
    audio_index = 0


    video_stream = next(
        (stream
         for stream in probe['streams'] if stream['codec_type'] == 'video'),
        None)
    if video_stream is None:
        logger.error('No video stream found')
        return {}

    (video_codec_type, video_width, video_height, video_framerate_num,
     video_framerate_denum, num_video_frame, duration) = get_video_stream_info(video_stream, probe)

    audio_stream = next(
        (stream
         for stream in probe['streams'] if stream['codec_type'] == 'audio'),
        None)
    if audio_stream is None:
        #At the moment, if the input video has no audio, it's not added to the database.
        logger.error('No audio stream found')
        return {}

    for stream in probe['streams']:
        if stream['codec_type'] == 'subtitle':
            logger.debug('Found Subtitles in the input stream')
            webvtt_ov_fullpath_tmp = os.path.splitext(video_full_path)[0]+'_ov_{}.vtt'.format(subtitles_index)
            try:
                extract_subtitle(video_full_path, webvtt_ov_fullpath_tmp, subtitles_index)
                webvtt_ov_fullpaths.append(webvtt_ov_fullpath_tmp)
            except:
                logger.error("Something went wrong with subtitle extraction, skipping track {}".format(subtitles_index))
            subtitles_index += 1
        elif stream['codec_type'] == 'audio':
            (audio_codec_type, audio_duration, lang) = get_audio_stream_info(stream, probe)
            audio_elementary_stream_path = "{}_{}.m4a".format(
                os.path.splitext(video_full_path)[0], audio_index)

            cache.set("ingestion_task_{}".format(video_full_path), "encoding audio", timeout=None)
            if "aac" in audio_codec_type:
                extract_audio(video_full_path, audio_elementary_stream_path, audio_index)
            else:
                aac_encoder(video_full_path, audio_elementary_stream_path, "/usr/progress/progress-log.txt", audio_index)
            cache.set("audio_total_duration", audio_duration, timeout=None)
            cache.set("ingestion_task_{}".format(video_full_path), "encoding audio", timeout=None)
            audio_tracks.append((audio_elementary_stream_path, lang))
            audio_index += 1

    dash_fragment_duration = 4000
    skip_high_layer_encoding = False
    
    output_fps_num = video_framerate_num
    output_fps_denum = video_framerate_denum
    logger.debug("dash_fragment_duration = {}".format(str(dash_fragment_duration)))

    '''if "h264" in video_codec_type:
        analysis_result = keyframe_analysis(video_full_path)
        if analysis_result[0]:
            logger.debug("Regular GoP Structure was detected, we are going to use the input without reecoding it")
            skip_high_layer_encoding = True
            dash_fragment_duration = float(analysis_result[1]) * (float(video_framerate_num)/float(video_framerate_denum))
            logger.debug("Gop Duration = {}".format(dash_fragment_duration))'''

    video_elementary_stream_path_high_layer = "{}_{}.264".format(
        os.path.splitext(video_full_path)[0], video_height)

    dash_output_directory = os.path.splitext(video_full_path)[0]
    temp_mpd = "{}/playlist.mpd".format(dash_output_directory)
    
    #https://stackoverflow.com/questions/5024114/suggested-compression-ratio-with-h-264
    high_layer_compression_ratio = int(
        os.getenv('HIGH_LAYER_QUALITY', 3))
    high_layer_bitrate = video_width * video_height * \
        24 * 4 * (high_layer_compression_ratio/100.0)
    logger.debug("high_layer_bitrate = {}".format(high_layer_bitrate))

    low_layer_bitrate = int(os.getenv('LOW_QUALITY_LAYER_BITRATE', 400000))
    low_layer_height = 0
    if ((video_height % 2.0) == 0):
        #We only encode low layer if lower resolution has the same aspect ratio as input
        low_layer_height = int(video_height / 2.0)

    video_elementary_stream_path_low_layer = "{}_low.264".format(
        os.path.splitext(video_full_path)[0])

    cache.set("video_frames_{}".format(video_full_path), num_video_frame, timeout=None)
    cache.set("ingestion_task_{}".format(video_full_path), "encoding video layer 1", timeout=None)


    if skip_high_layer_encoding:
        extract_video(video_full_path, video_elementary_stream_path_high_layer)
    else:
        h264_encoder(
            video_full_path,
            video_elementary_stream_path_high_layer, video_height, high_layer_bitrate , "/usr/progress/progress-log.txt", output_fps_num, output_fps_denum)

    video_tracks.append((video_elementary_stream_path_high_layer, video_height, high_layer_bitrate))

    if (low_layer_bitrate > 0 and low_layer_height > 0):
        try:
            cache.set("ingestion_task_{}".format(video_full_path), "encoding video layer 2", timeout=None)
            h264_encoder(
                video_full_path,
                video_elementary_stream_path_low_layer, low_layer_height, low_layer_bitrate, "/usr/progress/progress-log.txt", output_fps_num, output_fps_denum)
            video_tracks.append((video_elementary_stream_path_low_layer, low_layer_height, low_layer_bitrate))
        except:
            logger.error("An exception occured during low layer encoding, skip this layer")
            low_layer_bitrate = 0
            low_layer_height = 0


    relative_path = os.path.relpath(video_full_path, video_path)

    if not os.path.exists(dash_output_directory):
        os.mkdir(dash_output_directory)

    #Thumbnail creation
    thumbnail_fullpath = "{}/thumbnail.jpeg".format(dash_output_directory)

    thumbnail_relativepath = os.path.relpath(thumbnail_fullpath, video_path)
    if (os.path.isfile(thumbnail_fullpath) is False):
        generate_thumbnail(video_full_path, duration, thumbnail_fullpath)

    cache.set("ingestion_task_{}".format(video_full_path), "dashing", timeout=None)
    cache.delete("video_frames_{}".format(video_full_path))

    #Dash_packaging
    dash_packager(video_tracks, audio_tracks,
                  dash_output_directory, dash_fragment_duration, output_fps_num, output_fps_denum)

    for video in video_tracks:
        os.remove(video[0])
    #We remove all audio tracks except the first one (which will be used for audio/sub resync and deleted 
    #when Video (ORM) objects is deleted
    for audio in audio_tracks[1:]:
        os.remove(audio[0])

    if not keep_files:
        os.remove(video_full_path)

    relative_path = os.path.relpath(temp_mpd, video_path)
    size_in_bytes = get_size(video_dir)
    size_in_megabytes = math.ceil(float(size_in_bytes) * 0.000001)

    remote_video_url = os.path.join(remote_url, relative_path)
    remote_thumbnail_url = os.path.join(remote_url, thumbnail_relativepath)
    video_info = {
        'remote_video_url': remote_video_url,
        'video_codec_type': video_codec_type,
        'audio_codec_type': audio_codec_type,
        'audio_path': audio_tracks[0][0],
        'video_height': video_height,
        'video_width': video_width,
        'size_in_megabytes' : size_in_megabytes,
        'remote_thumbnail_url': remote_thumbnail_url,
        'ov_subtitles': webvtt_ov_fullpaths,
        'video_full_path': video_full_path,
        'mpd_path': temp_mpd
    }

    #File info creation
    fileinfo_path = "{}/fileinfo.json".format(dash_output_directory)
    createfileinfo(fileinfo_path, video_info)

    return video_info


def get_video_type_and_info(video_path):
    """ # Uses subliminal to parse information from filename.

    Subliminal tells us if the video is a serie or not.
    If not, we assume it to be a movie, which is not necesarly the case (e.g. documentary, simple video).
    We use string.capwords() on title strings for consistency of capitalization.
    The subliminal fromname function as a bug when the input string begins with 1-, as a quick fix, we use a regular expression to
    get rid of the problematic characters. A future fix coulb be to be use imdb api for disambiguation.

    Args:
    video_path: full path to the video (eg: /Videos/folder1/video.mp4)

    Returns: dict containing video type and info

    """
    filename = os.path.basename(video_path)
    if re.match(r'(\d*(\-|\.) .*)', filename):
        filename = re.sub(r'(\d*(\-|\.) )', '', filename, 1)
    try:
        video = subliminal.Video.fromname(filename)
    except ValueError:
        #This usually happens when there is not enough data for subliminal to guess.
        return {
            'type': 'Movie',
            'title': string.capwords(filename),
        }

    if hasattr(video, 'series'):
        return {
            'type': 'Series',
            'title': string.capwords(video.series),
            'season': video.season,
            'episode': video.episode,
        }
    elif hasattr(video, 'title'):
        return {
            'type': 'Movie',
            'title': string.capwords(video.title),
        }
