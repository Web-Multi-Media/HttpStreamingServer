from django.test import Client, TestCase
from StreamServerApp.media_management.frame_analyzer import keyframe_analysis
from StreamServerApp.media_management.encoder import h264_encoder, aac_encoder
from StreamServerApp.media_management.dash_packager import dash_packager
from clint.textui import progress
import os
import shutil
import requests


def download_file(url, folder_name):
    local_filename = url.split('/')[-1]
    path = os.path.join("/{}/{}".format(folder_name, local_filename))
    with requests.get(url, stream=True) as r:
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                      expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()

    return local_filename


class TestDash(TestCase):
    def setUp(self):
        print("Init keyframe_analysis test ")

    def test_dash_packaging(self):
        input_height = 720
        low_layer_height = int(input_height / 2.0)
        high_layer_height = 720
        high_layer_bitrate = 1800000
        low_layer_bitrate = 800000
        path_to_highlayer = "/usr/src/app/Videos/lebowsky_720.264"
        path_to_lowlayer = "/usr/src/app/Videos/lebowsky_low.264"

        h264_encoder(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
            path_to_highlayer, high_layer_height, high_layer_bitrate)
        h264_encoder(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
            path_to_lowlayer, low_layer_height, low_layer_bitrate)
        
        aac_encoder(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
            "/usr/src/app/Videos/lebowsky_track1.m4a")

        aac_encoder(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
            "/usr/src/app/Videos/lebowsky_track2.m4a")

        video_list = [(path_to_highlayer, high_layer_bitrate, high_layer_height),
                      (path_to_lowlayer, low_layer_bitrate, low_layer_height),
                     ]
        
        audio_list = [("/usr/src/app/Videos/lebowsky_track1.m4a", "eng"),
                      ("/usr/src/app/Videos/lebowsky_track2.m4a", "fr")
                     ]

        dash_packager(video_list, audio_list, "/usr/src/app/Videos/lebowskydash/")

        video_list = [(path_to_highlayer, high_layer_bitrate, high_layer_height)]

        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash/segment_720p_1.m4s"), True)
        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash/segment_{}p_1.m4s".format(low_layer_height)), True)

        dash_packager(video_list, audio_list,
                      "/usr/src/app/Videos/lebowskydash2/")

        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash2/segment_720p_1.m4s"), True)
        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash2/segment_{}p_1.m4s".format(low_layer_height)), False)
