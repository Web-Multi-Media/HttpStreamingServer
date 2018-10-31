from django.http import HttpResponse
from django.template import loader
from os import listdir
from os.path import isfile, join
from django.conf import settings
from StreamServerApp.models import Video


def index(request):
    template = loader.get_template('StreamServerApp/index.html')
    mypath = settings.SERVER_VIDEO_DIR

    for f in listdir(mypath):
        if isfile(join(mypath, f)) and f.endswith(".mp4"):
            v = Video(name="f", baseurl=settings.REMOTE_VIDEO_DIR + "/" + f)
            v.save()

    return HttpResponse(template.render({}, request))


def rendervideo(request):
    template = loader.get_template('StreamServerApp/ShowVideo.html')
    VidNumberStr = request.GET.get('VideoNumber')
    context = {}
    pks = list(Video.objects.values_list('pk', flat=True))
    if not VidNumberStr:
        # Return first video urls with the "neighboors" primary key
        url = Video.objects.get(pk=pks[0]).baseurl
        previd = pks[len(pks) - 1]
        nextid = pks[1]
        context = {
            'url': url,
            'prevId': previd,
            'nextId': nextid
        }
    else:
        # Return requested video urls with the two neighboors primary keys
        Vidpk = int(VidNumberStr)
        url = Video.objects.get(pk=Vidpk).baseurl
        if pks.index(Vidpk) == len(pks) - 1:
            nextid = pks[0]
        else:
            nextid = pks[pks.index(Vidpk) + 1]
        if pks.index(Vidpk) == 0:
            previd = pks[len(pks) - 1]
        else:
            previd = pks[pks.index(Vidpk) - 1]
        context = {
            'url': url,
            'prevId': previd,
            'nextId': nextid
        }
    return HttpResponse(template.render(context, request))
