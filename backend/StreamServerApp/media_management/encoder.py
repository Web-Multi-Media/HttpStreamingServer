
from StreamServerApp.media_management.subprocess_wrapper import run_subprocess


def h264_encoder(filename, output, resolutionH, bitrate, progress_log, frameratenum, frameratedenum):
    command = ["ffmpeg", "-progress", progress_log, "-y", "-i", filename, "-filter:v",  "scale=-2:{}".format(resolutionH),
               "-c:v", "libx264",  "-b:v", str(int(bitrate)),
               "-r", "{}/{}".format(frameratenum, frameratedenum), "-x264opts", "keyint=48:min-keyint=48:no-scenecut",
               "-movflags", "faststart", "-bufsize", "8600k",
               "-pix_fmt", "yuv420p", "-profile:v", "main", "-preset", "veryfast",
               "-an", "{}".format(output)]

    run_subprocess(command)


def aac_encoder(filename, output, progress_log,  track_number=0):

    command = ["ffmpeg", "-progress", progress_log, "-y", "-i", filename,
               "-map", "0:a:{}".format(track_number), "-filter:a", "loudnorm", "-vn",  "-c:a", "aac",  "-b:a", "128k",
               "-ar",  "48000", "-ac", "2",
               "{}".format(output)]

    run_subprocess(command)


def extract_audio(filename, output, track_number=0):
    command = ["ffmpeg", "-y", "-i", filename, "-vn", "-acodec", "copy", "-map", "0:a:{}".format(track_number),
               output]
    run_subprocess(command)


def extract_video(filename, output, track_number=0):
    command = ["ffmpeg", "-y", "-i", filename, "-an", "-vcodec", "copy", "-map", "0:v:{}".format(track_number),
               output]
    run_subprocess(command)
