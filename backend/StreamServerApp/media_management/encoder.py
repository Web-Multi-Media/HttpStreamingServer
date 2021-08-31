import os
import subprocess
import json


def h264_encoder(filename, output, resolutionH, bitrate):
    command = 'ffmpeg -y -i "{filename}" -filter:v scale=-2:"{resolution}" -c:v libx264 -b:v "{bitrate}" \
            -r 24 -x264opts \'keyint=48:min-keyint=48:no-scenecut\' \
            -movflags faststart -bufsize 8600k \
            -pix_fmt yuv420p -profile:v main -preset veryfast -an  "{outputfile}"'.format(
        outputfile=output, resolution=resolutionH, bitrate=bitrate, filename=filename)

    print(command)

    response_json = subprocess.check_output(command, shell=True, stderr=None)


def aac_encoder(filename, output):
    command = 'ffmpeg -y -i "{filename}" -map 0:1? -vn -c:a aac -b:a 128k -ar 48000 -ac 2 \
                "{outputfile}"'.format(outputfile=output, filename=filename)

    print(command)

    response_json = subprocess.check_output(command, shell=True, stderr=None)


def extract_audio(filename, output):
    command = 'ffmpeg -y -i "{filename}" -vn -acodec copy \
                "{outputfile}"'.format(outputfile=output, filename=filename)

    print(command)

    response_json = subprocess.check_output(command, shell=True, stderr=None)