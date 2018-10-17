from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('StreamServerApp/index.html')
    files = ['foo1', 'foo2', 'foo3']
    context = {
        'files': files,
    }
    return HttpResponse(template.render(context, request))
