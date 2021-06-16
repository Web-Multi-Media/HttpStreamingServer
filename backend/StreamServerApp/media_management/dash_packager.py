import os
import subprocess
import json


def dash_packager(video_layer, audio_layer, outputdirectory):
    command = 'MP4Box -dash 4000 -frag 4000 -rap \
        -segment-name \'segment_$RepresentationID$_\' -fps 24 \
        "{video_layer}"#video \
        "{audio_layer}"#audio:id=English:role=main \
        -out "{outputdirectory}"/playlist.mpd'.format(
        video_layer=video_layer,
        audio_layer=audio_layer,
        outputdirectory=outputdirectory)

    print(command)

    response_json = subprocess.check_output(command, shell=True, stderr=None)