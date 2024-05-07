from django.test import Client, TestCase
from StreamServerApp.media_management.frame_analyzer import keyframe_analysis
from StreamServerApp.media_management.media_analyzer import get_video_stream_info, get_media_file_info
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

    def test_keyframe_analysis(self):
        analysis_result = keyframe_analysis(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4")
        self.assertEqual(analysis_result, (False, 997))
        analysis_result = keyframe_analysis(
            "/usr/src/app/Videos/folder1/Best_Movie_Ever.avi")
        analysis_result = keyframe_analysis(
            "/usr/src/app/Videos/folder1/Matrix.mp4")
        analysis_result = keyframe_analysis(
            "/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S04E18.HDTV.x264-LOL.mp4")
        self.assertEqual(analysis_result, (True, 18))
        analysis_result = keyframe_analysis(
            "/usr/src/app/Videos/folder2/The.Blues.Brothers.1980.1080p.BrRip.x264.bitloks.YIFY.mkv")

    def test_video_analysis_1(self):
        test_files = ["/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
                      "/usr/src/app/Videos/folder2/The.Blues.Brothers.1980.1080p.BrRip.x264.bitloks.YIFY.mkv",
                      "/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S04E18.HDTV.x264-LOL.mp4",
                      "/usr/src/app/Videos/folder2/Fantastic.Beasts.The.Crimes.Of.Grindelwald.2018.1080p.WEBRip.mp4",
                      ]
        
        for file in test_files:
            probe = get_media_file_info(file)
         
            video_stream = next(
                (stream
                    for stream in probe['streams'] if stream['codec_type'] == 'video'),
                None)

            (video_codec_type, video_width, video_height, video_framerate_num,
                video_framerate_denum, num_video_frame, duration) = get_video_stream_info(video_stream, probe)

            self.assertNotEqual(num_video_frame, None)
            self.assertNotEqual(duration, None)
        

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
            path_to_highlayer, high_layer_height, high_layer_bitrate, "progress_video1", 24, 1)
        h264_encoder(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
            path_to_lowlayer, low_layer_height, low_layer_bitrate, "progress_video2", 24, 1)
        
        aac_encoder(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
            "/usr/src/app/Videos/lebowsky_track1.m4a", "progress_audio1")

        aac_encoder(
            "/usr/src/app/Videos/The.Big.Lebowski.1998.720p.BrRip.x264.YIFY.mp4",
            "/usr/src/app/Videos/lebowsky_track2.m4a", "progress_audio2")

        video_list = [(path_to_highlayer, high_layer_bitrate, high_layer_height),
                      (path_to_lowlayer, low_layer_bitrate, low_layer_height),
                     ]
        
        audio_list = [("/usr/src/app/Videos/lebowsky_track1.m4a", "eng"),
                      ("/usr/src/app/Videos/lebowsky_track2.m4a", "fr")
                     ]

        dash_packager(video_list, audio_list, "/usr/src/app/Videos/lebowskydash/", 4000, 24, 1)

        video_list = [(path_to_highlayer, high_layer_bitrate, high_layer_height)]

        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash/segment_720p_1.m4s"), True)
        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash/segment_{}p_1.m4s".format(low_layer_height)), True)

        dash_packager(video_list, audio_list,
                      "/usr/src/app/Videos/lebowskydash2/", 4000, 24, 1)

        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash2/segment_720p_1.m4s"), True)
        self.assertEqual(os.path.isfile(
            "/usr/src/app/Videos/lebowskydash2/segment_{}p_1.m4s".format(low_layer_height)), False)
