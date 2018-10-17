from django.http import HttpResponse
from django.template import loader
from os import listdir
from os.path import isfile, join
from django.conf import settings


def index(request):
    template = loader.get_template('StreamServerApp/index.html')
    mypath = settings.VIDEO_DIR
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    context = {
        'files': files,
    }
    return HttpResponse(template.render(context, request))
