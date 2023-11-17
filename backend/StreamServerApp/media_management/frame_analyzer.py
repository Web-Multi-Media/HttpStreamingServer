import os
import subprocess
import json
from StreamServerApp.media_management.subprocess_wrapper import run_subprocess



class BFrame(object):
    def __repr__(self, *args, **kwargs):
        return "B"

    def __str__(self, *args, **kwargs):
        return repr(self)


class PFrame(object):
    def __repr__(self, *args, **kwargs):
        return "P"

    def __str__(self, *args, **kwargs):
        return repr(self)


class IFrame(object):
    def __init__(self):
        self.key_frame = False

    def __repr__(self, *args, **kwargs):
        if self.key_frame:
            return "I"
        else:
            return "i"

    def __str__(self, *args, **kwargs):
        return repr(self)


class GOP(object):
    def __init__(self):
        self.closed = False
        self.frames = []

    def add_frame(self, frame):
        self.frames.append(frame)

        if isinstance(frame, IFrame) and frame.key_frame:
            self.closed = True

    def __repr__(self, *args, **kwargs):
        frames_repr = ''

        for frame in self.frames:
            frames_repr += str(frame)

        gtype = 'CLOSED' if self.closed else 'OPEN'

        return 'GOP: {frames} {count} {gtype}'.format(frames=frames_repr,
                                                      count=len(self.frames),
                                                      gtype=gtype)

"""
check keyframe structure. Return value is a tuple whose first value is a boolean indicates if keyframe structure is regular
and second value is the keyframe structure period in frames (valid only if structure is regular).
The following asumption is made: If the gop Structure is regular for the first 40 sec (hence the "%+40"), we assume it is for the rest of the video.
:rtype: (Bool, int)
"""


def keyframe_analysis(filename):
    command = ["ffprobe",  "-v", "quiet", "-select_streams", "v:0", "-read_intervals", "%+40", "-show_entries", "stream=nb_frames",
               "-show_frames", "-print_format", "json",  "{}".format(filename)]
    with open('frame_analysis.log', "w") as outfile:
        stdout = run_subprocess(command)
        d = json.loads(stdout.decode('utf-8'))
        json.dump(d, outfile)

    # Opening JSON file
    f = open('frame_analysis.log')

    # returns JSON object as
    # a dictionary
    frames = json.load(f)["frames"]

    gops_duration_in_frames = []
    gops = []
    gop = GOP()
    gops.append(gop)

    for jframe in frames:
        if jframe["media_type"] == "video":

            frame = None

            if jframe["pict_type"] == 'I':
                if len(gop.frames):
                    gops_duration_in_frames.append(len(gop.frames))
                    # GOP open and new iframe. Time to close GOP
                    gop = GOP()
                    gops.append(gop)

                frame = IFrame()
                if jframe["key_frame"] == 1:
                    frame.key_frame = True
            elif jframe["pict_type"] == 'P':
                frame = PFrame()
            elif jframe["pict_type"] == 'B':
                frame = BFrame()

            frame.json = jframe
            gop.add_frame(frame)

    gops_duration_in_frames.append(len(gop.frames))

    regular_duration = False

    if gops_duration_in_frames.count(gops_duration_in_frames[0]) == len(gops_duration_in_frames) - 1:
        regular_duration = True

    #for gop in gops:
    #    print(gop)

    return (regular_duration, gops_duration_in_frames[0])