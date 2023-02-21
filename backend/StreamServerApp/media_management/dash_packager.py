import os
import subprocess
import json


def dash_packager(videolist, audiolist,   outputdirectory):
    command = 'MP4Box -dash 4000 -frag 4000 -rap \
-segment-name \'segment_$RepresentationID$_\' -fps 24 '

    for video in videolist:
        command += '"{video_layer}"#video:id={height}p:#Bitrate={bitrate} '.format(
            video_layer=video[0], bitrate=video[1], height=video[2])

    for i, audio in enumerate(audiolist):
        command += '"{audio_layer}"#audio:id=audio{id}":role={role}" '.format(
            audio_layer=audio[0], id=i, role="main" if i == 0 else "alternate")

    command += ' -out "{outputdirectory}/playlist.mpd"'.format(
        outputdirectory=outputdirectory)

    print(command)

    response_json = subprocess.check_output(command, shell=True, stderr=None)
