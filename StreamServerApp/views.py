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
    if not VidNumberStr:
    #Return first video urls with the two neighboors id
      url=Video.objects.first().baseurl
      context = {
             'url': url,
             'prevId': 0,
             'nextId': 1
      }
    return HttpResponse(template.render(context, request))
