

def timecodeToSec(s_timecode: str):
    hour, minute, second = s_timecode.split(':')
    return 3600 * int(hour) + 60 * int(minute) + int(second.split('.')[0])
