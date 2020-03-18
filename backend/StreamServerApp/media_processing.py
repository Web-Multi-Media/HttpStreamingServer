import os
import subprocess
from StreamingServer.settings import customstderr, customstdout

def run_ffmpeg_process(cmd):
    completed_process_instance = subprocess.run(cmd, stdout=customstdout,
                                            stderr=customstderr)
    if completed_process_instance.returncode != 0:
        print("An error occured while running ffmpeg subprocess")
        print(completed_process_instance.stderr)
        print(completed_process_instance.stdout)
        raise Exception('ffmpeg_error', 'error')

def convert_subtitles_to_webvtt(input_file, output_file):
    """ # Uses ffmpeg subprocess to convert subtitles to webvtt
    
    Args:
    input_file: full path to the input subtitle (eg: /Videos/folder1/sub.srt)
    output_file: full path to the output webvtt file (eg: /Videos/folder1/sub.vtt)

    Returns: dict containing video type and info

    Throw an exception if the return value of the subprocess is different than 0

    """
    cmd = ["ffmpeg", "-n", "-sub_charenc", "UTF-8", "-i", input_file, output_file]
    if(os.path.isfile(output_file) == False):
        run_ffmpeg_process(cmd)

def extract_subtitle(input_file, output_file):
    """ # Uses ffmpeg subprocess to extract subtitles from a video and convert it to webvtt
    
    Args:
    input_file: full path to the input video (eg: /Videos/folder1/video.mp4)
    output_file: full path to the output webvtt file (eg: /Videos/folder1/sub.vtt)

    Returns: dict containing video type and info

    Throw an exception if the return value of the subprocess is different than 0

    """
    cmd = ["ffmpeg", "-n", "-sub_charenc", "UTF-8", "-i", input_file,"-map", "0:s:0", output_file]
    if(os.path.isfile(output_file) == False):
        run_ffmpeg_process(cmd)

def transmux_to_mp4(input_file, output_file, with_audio_reencode=False):
    """ # Uses ffmpeg subprocess to transmux to mp4
    
    Args:
    input_file: full path to the input video (eg: /Videos/folder1/video.mp4)
    output_file: full path to the output video (eg: /Videos/folder1/video.mp4)

    Returns: dict containing video type and info

    Throw an exception if the return value of the subprocess is different than 0

    """
    if with_audio_reencode:
        print(
            "Audio codec is not aac, audio reencoding is necessary (This might take a long time)")
        cmd = ["ffmpeg", "-i", input_file,
                "-acodec", "aac", "-vcodec", "copy", output_file]
    else:
        cmd = ["ffmpeg", "-i", input_file,
                "-codec", "copy",  output_file]

    if(os.path.isfile(output_file) == False):
        run_ffmpeg_process(cmd)