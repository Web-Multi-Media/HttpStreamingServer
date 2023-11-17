import os
import subprocess
import json
from .subprocess_wrapper import run_subprocess


def dash_packager(videolist, audiolist, outputdirectory, segment_duration, fpsnum, fpsdenum):
    command = ["MP4Box",  "-dash",  str(segment_duration), "-frag",  str(segment_duration), 
                "-rap", "-segment-name",  "segment_$RepresentationID$_" , "-init-segment-ext",
                "null",  "-fps",  "{}/{}".format(fpsnum, fpsdenum)]


    for video in videolist:
        command.append('{video_layer}#video:id={height}p:#Bitrate={bitrate} '.format(
            video_layer=video[0], bitrate=video[1], height=video[2]))

    for i, audio in enumerate(audiolist):
        command.append('{audio_layer}#audio:id=audio{id}":role={role}" '.format(
            audio_layer=audio[0], id=i, role="main" if i == 0 else "alternate"))

    command.extend(["-out", "{outputdirectory}/playlist.mpd".format(
        outputdirectory=outputdirectory)])

    run_subprocess(command)