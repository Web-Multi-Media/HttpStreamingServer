from StreamServerApp.media_management.timecode import timecodeToSec


def get_audio_stream_info(stream, general_streams_props):
    duration = None
    audio_codec_type = stream['codec_name']
    if "duration" in stream:
        duration =  stream["duration"]
    elif "tags" in stream:
        if "DURATION" in stream["tags"]:
            duration = timecodeToSec(stream["tags"]["DURATION"])
        elif 'duration' in general_streams_props['format']:
            duration = general_streams_props['format']['duration']
    lang = "und"
    try:
        lang = stream["tags"]["language"]
    except KeyError:
        lang = "und"
    return (audio_codec_type, duration, lang)

def get_video_stream_info(video_stream, general_streams_props):
    video_codec_type = video_stream['codec_name']
    video_width = video_stream['width']
    video_height = video_stream['height']
    video_framerate_num, video_framerate_denum = video_stream["avg_frame_rate"].split(
        '/')

    num_video_frame = None
    duration = None
    if "nb_frames" in video_stream:
        num_video_frame = video_stream['nb_frames']
    elif "tags" in video_stream:
        # MKV doens't signal number of frames, lets compute it
        if "DURATION" in video_stream["tags"]:
            total_sec = timecodeToSec(video_stream["tags"]["DURATION"])
            if '/' in video_stream["avg_frame_rate"]:
                num_video_frame = int(
                    (float(total_sec) * float(video_framerate_num))/float(video_framerate_denum))
            else:
                num_video_frame = int(
                    float(total_sec) * float(video_stream["avg_frame_rate"]))

    if 'duration' in video_stream:
        duration = float(video_stream['duration'])
    elif 'duration' in general_streams_props['format']:
        duration = float(general_streams_props['format']['duration'])

    return (video_codec_type, video_width, video_height, video_framerate_num, video_framerate_denum, num_video_frame, duration)
