from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.postgres.search import TrigramSimilarity
from django.core import serializers
from django.core.paginator import Paginator
from django.conf import settings

from StreamServerApp.models import Video
from StreamServerApp import utils


def index(request):
    return render(request, "index.html")


def get_videos(request):
    qs = Video.objects.all()
    paginator = Paginator(qs, settings.PAGE_SIZE)

    page = request.GET.get('page', 0)
    videos = paginator.get_page(page)
    qs_json = serializers.serialize('json', videos)

    return HttpResponse(qs_json, content_type='application/json')


def search_video(request):
    print(request)
    query = request.GET.get('q', '')

    if query == '':
        qs_results = Video.objects.all()
    else:
        qs_results = Video.objects.annotate(similarity=TrigramSimilarity('name', query)) \
                                .filter(similarity__gte=0.01) \
                                .order_by('-similarity')

    paginator = Paginator(qs_results, settings.PAGE_SIZE)
    page = request.GET.get('page', 0)
    videos = paginator.get_page(page)

    qs_json = serializers.serialize('json', videos)

    return HttpResponse(qs_json, content_type='application/json')


def update_database(request):
    print("updating database")
    utils.delete_DB_Infos()
    utils.populate_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
