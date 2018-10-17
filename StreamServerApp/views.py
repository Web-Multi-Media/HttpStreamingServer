from django.http import HttpResponse
from django.template import loader
from os import listdir
from os.path import isfile, join
from django.conf import settings


def index(request):
    template = loader.get_template('StreamServerApp/index.html')
    mypath = settings.SERVER_VIDEO_DIR

    files = []

    for f in listdir(mypath):
        if isfile(join(mypath, f)) and f.endswith(".mp4"):
            files.append(settings.REMOTE_VIDEO_DIR + "/" + f)

    context = {
        'fileid': 1,
        'numids': len(files),
    }
    return HttpResponse(template.render(context, request))


def rendervideo(request):
    template = loader.get_template('StreamServerApp/ShowVideo.html')
    videoNumber = int(request.GET.get('VideoNumber'))
    mypath = settings.SERVER_VIDEO_DIR

    files = []

    for f in listdir(mypath):
        if isfile(join(mypath, f)) and f.endswith(".mp4"):
            files.append(settings.REMOTE_VIDEO_DIR + "/" + f)

    if (videoNumber > 0 and videoNumber <= len(files)):
        context = {
            'file': files[videoNumber],
        }
        return HttpResponse(template.render(context, request))
