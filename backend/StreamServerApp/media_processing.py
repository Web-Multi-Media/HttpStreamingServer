import os
import subprocess
import json

import re
import subliminal
import ffmpeg
import sys
import string
from StreamServerApp.media_management.encoder import h264_encoder, aac_encoder, extract_audio
from StreamServerApp.media_management.dash_packager import dash_packager
from StreamServerApp.media_management.fileinfo import createfileinfo, readfileinfo
from StreamServerApp.media_management.subprocess_wrapper import run_ffmpeg_process



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
        run_ffmpeg_process(cmd)


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
        run_ffmpeg_process(cmd)


def transmux_to_mp4(input_file, output_file, with_audio_reencode=False):
    """ # Uses ffmpeg subprocess to transmux to mp4
    
    Args:
    input_file: full path to the input video (eg: /Videos/folder1/video.mp4)
    output_file: full path to the output video (eg: /Videos/folder1/video.mp4)

    Returns: void

    Throw an exception if the return value of the subprocess is different than 0

    """
    if with_audio_reencode:
        print(
            "Audio codec is not aac, audio reencoding is necessary (This might take a long time)")
        cmd = ["ffmpeg", "-i", input_file,
                "-acodec", "aac", "-vcodec", "copy", "-movflags", "+faststart", output_file]
    else:
        cmd = ["ffmpeg", "-i", input_file,
                "-codec", "copy", "-movflags", "+faststart", output_file]

    if not os.path.isfile(output_file):
        run_ffmpeg_process(cmd)


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
        run_ffmpeg_process(cmd)


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

        this functions will only add videos to the database if
        they are encoded with h264/AAC codec
    """
    print("processing {}".format(video_full_path))
    try:
        probe = ffmpeg.probe(video_full_path)
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        raise

    video_stream = next(
        (stream
         for stream in probe['streams'] if stream['codec_type'] == 'video'),
        None)
    if video_stream is None:
        print('No video stream found', file=sys.stderr)
        return {}


    video_codec_type = video_stream['codec_name']
    video_width = video_stream['width']
    video_height = video_stream['height']

    if 'duration' in video_stream:
        duration = float(video_stream['duration'])
    elif 'duration' in probe['format']:
        duration = float(probe['format']['duration'])

    audio_stream = next(
        (stream
         for stream in probe['streams'] if stream['codec_type'] == 'audio'),
        None)
    if audio_stream is None:
        #At the moment, if the input video has no audio, it's not added to the database.
        print('No audio stream found', file=sys.stderr)
        return {}

    webvtt_ov_fullpaths = []
    subtitles_stream = None
    subtitles_index = 0 
    for stream in probe['streams']:
        if stream['codec_type'] == 'subtitle':
            print('Found Subtitles in the input stream')
            webvtt_ov_fullpath_tmp = os.path.splitext(video_full_path)[0]+'_ov_{}.vtt'.format(subtitles_index)
            print(video_full_path)
            print(webvtt_ov_fullpath_tmp)
            try:
                extract_subtitle(video_full_path, webvtt_ov_fullpath_tmp, subtitles_index)
                webvtt_ov_fullpaths.append(webvtt_ov_fullpath_tmp)
            except:
                print("Something went wrong with subtitle extraction, skipping track {}".format(subtitles_index))
            subtitles_index += 1

    audio_codec_type = audio_stream['codec_name']
    audio_elementary_stream_path = "{}.m4a".format(
        os.path.splitext(video_full_path)[0])

    video_elementary_stream_path_high_layer = "{}_{}.264".format(
        os.path.splitext(video_full_path)[0], video_height)

    dash_output_directory = os.path.splitext(video_full_path)[0]
    temp_mpd = "{}/playlist.mpd".format(dash_output_directory)

    if "aac" in audio_codec_type:
        extract_audio(video_full_path, audio_elementary_stream_path)
    else:
        aac_encoder(video_full_path, audio_elementary_stream_path)
    
    #https://stackoverflow.com/questions/5024114/suggested-compression-ratio-with-h-264
    high_layer_compression_ratio = int(
        os.getenv('HIGH_LAYER_COMPRESSION_RATIO_IN_PERCENTAGE', 7))
    high_layer_bitrate = video_width * video_height * \
        24 * 4 * (high_layer_compression_ratio/100.0)
    print("high_layer_bitrate = {}".format(high_layer_bitrate))
    low_layer_bitrate = int(os.getenv('480P_LAYER_BITRATE', 400000))
    low_layer_height = 0
    if ((video_height % 2.0) == 0):
        #We only encode low layer if lower resolution has the same aspect ratio as input
        low_layer_height = int(video_height / 2.0)

    video_elementary_stream_path_low_layer = "{}_low.264".format(
        os.path.splitext(video_full_path)[0])

    h264_encoder(
        video_full_path,
        video_elementary_stream_path_high_layer, video_height, high_layer_bitrate)

    if (low_layer_bitrate > 0 and low_layer_height > 0):
        try:
            h264_encoder(
                video_full_path,
                video_elementary_stream_path_low_layer, low_layer_height, low_layer_bitrate)
        except:
            print("An exception occured during low layer encoding, skip this layer")
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

    #Dash_packaging
    dash_packager(video_elementary_stream_path_low_layer, low_layer_bitrate, low_layer_height,
                  video_elementary_stream_path_high_layer, high_layer_bitrate, video_height, audio_elementary_stream_path,
                  dash_output_directory)

    os.remove(video_elementary_stream_path_high_layer)
    if (low_layer_bitrate > 0 and low_layer_height > 0):
        os.remove(video_elementary_stream_path_low_layer)

    if not keep_files:
        os.remove(video_full_path)

    relative_path = os.path.relpath(temp_mpd, video_path)

    remote_video_url = os.path.join(remote_url, relative_path)
    remote_thumbnail_url = os.path.join(remote_url, thumbnail_relativepath)
    video_info = {
        'remote_video_url': remote_video_url,
        'video_codec_type': video_codec_type,
        'audio_codec_type': audio_codec_type,
        'audio_path': audio_elementary_stream_path,
        'video_height': video_height,
        'video_width': video_width,
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
