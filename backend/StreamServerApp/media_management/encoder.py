
from StreamServerApp.media_management.subprocess_wrapper import run_ffmpeg_process


def h264_encoder(filename, output, resolutionH, bitrate, progress_log):
    command = ["ffmpeg", "-progress", progress_log, "-y", "-i", filename, "-filter:v",  "scale=-2:{}".format(resolutionH),
               "-c:v", "libx264",  "-b:v", str(int(bitrate)),
               "-r", "24", "-x264opts", "keyint=48:min-keyint=48:no-scenecut",
               "-movflags", "faststart", "-bufsize", "8600k",
               "-pix_fmt", "yuv420p", "-profile:v", "main", "-preset", "veryfast",
               "-an", "{}".format(output)]

    print(command)
    run_ffmpeg_process(command)


def aac_encoder(filename, output, progress_log,  track_number=0):

    command = ["ffmpeg", "-progress", progress_log, "-y", "-i", filename,
               "-map", "0:a:{}".format(track_number), "-filter:a", "loudnorm", "-vn",  "-c:a", "aac",  "-b:a", "128k",
               "-ar",  "48000", "-ac", "2",
               "{}".format(output)]

    print(command)
    run_ffmpeg_process(command)


def extract_audio(filename, output, track_number=0):
    print("Extracting Audio from {}".format(filename))
    command = ["ffmpeg", "-y", "-i", filename, "-vn", "-acodec", "copy", "-map", "0:a:{}".format(track_number),
               output]
    print(command)
    run_ffmpeg_process(command)
