from django.http import HttpResponse
from django.template import loader
from os import listdir
from os.path import isfile, join
from django.conf import settings
from StreamServerApp.models import Video

has_db_load = False


def index(request):
    template = loader.get_template('StreamServerApp/index.html')
    my_path = settings.SERVER_VIDEO_DIR
    global has_db_load

    if not has_db_load:
        for f in listdir(my_path):
            if isfile(join(my_path, f)) and f.endswith(".mp4"):
                v = Video(name="f", baseurl=settings.REMOTE_VIDEO_DIR + "/" + f)
                v.save()
        has_db_load = True
    return HttpResponse(template.render({}, request))


def rendervideo(request):
    template = loader.get_template('StreamServerApp/ShowVideo.html')
    vid_number_str = request.GET.get('VideoNumber')
    context = {}
    pks = list(Video.objects.values_list('pk', flat=True))
    if not vid_number_str:
        # Return first video urls with the "neighboors" primary key
        url = Video.objects.get(pk=pks[0]).baseurl
        prev_id = pks[len(pks) - 1]
        next_id = pks[1]
        context = {
            'url': url,
            'prevId': prev_id,
            'nextId': next_id
        }
    else:
        # Return requested video urls with the two neighboors primary keys
        vid_primary_key = int(vid_number_str)
        url = Video.objects.get(pk=vid_primary_key).baseurl
        if pks.index(vid_primary_key) == len(pks) - 1:
            nextid = pks[0]
        else:
            nextid = pks[pks.index(vid_primary_key) + 1]
        if pks.index(vid_primary_key) == 0:
            previd = pks[len(pks) - 1]
        else:
            previd = pks[pks.index(vid_primary_key) - 1]
        context = {
            'url': url,
            'prevId': previd,
            'nextId': nextid
        }
    return HttpResponse(template.render(context, request))
