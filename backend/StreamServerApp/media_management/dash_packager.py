import os
import subprocess
import json


def dash_packager(video_layer_480p, low_layer_bitrate, video_layer_high_quality, high_layer_bitrate, high_layer_resolution, audio_layer, outputdirectory):
    command = 'MP4Box -dash 4000 -frag 4000 -rap \
-segment-name \'segment_$RepresentationID$_\' -fps 24 '

    if low_layer_bitrate > 0:
        command += '"{video_layer_low}"#video:id=480p:#Bitrate={low_layer_bitrate} '.format(
            video_layer_low=video_layer_480p, low_layer_bitrate=low_layer_bitrate)

    command += '"{video_layer_high}"#video:id={high_layer_resolution}p:#Bitrate={high_layer_bitrate} \
"{audio_layer}"#audio:id=English:role=main \
-out "{outputdirectory}"/playlist.mpd'.format(
        low_layer_bitrate=low_layer_bitrate,
        high_layer_bitrate=high_layer_bitrate,
        high_layer_resolution=high_layer_resolution,
        video_layer_high=video_layer_high_quality,
        audio_layer=audio_layer,
        outputdirectory=outputdirectory)

    print(command)

    response_json = subprocess.check_output(command, shell=True, stderr=None)
