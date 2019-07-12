from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from StreamServerApp.models import Video
from django.contrib.postgres.search import TrigramSimilarity
from django.core import serializers
from StreamServerApp import utils


def index(request):
    return render(request, "index.html")

def get_videos(request):
    qs = Video.objects.all()
    qs_json = serializers.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')


def search_video(request):
    print(request)
    query = request.GET.get('q', '')

    if query == '':
        qs = Video.objects.all()
        qs_json = serializers.serialize('json', qs)
        return HttpResponse(qs_json, content_type='application/json')


    # ANOTHER EXAMPLE:
    # vector = SearchVector('name', weight='A') + SearchVector('description', weight='C')
    # query = SearchQuery(query)
    # qs_results = TaxonomyNode.objects.filter(taxonomy__dataset=dataset)\
    #                                  .annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3)\
    #                                  .order_by('rank')

    qs_results = Video.objects.annotate(similarity=TrigramSimilarity('name', query)) \
                              .filter(similarity__gte=0.2) \
                              .order_by('-similarity')

    qs_json = serializers.serialize('json', qs_results)

    return HttpResponse(qs_json, content_type='application/json')

def update_database(request):
    print("updating database")
    utils.delete_DB_Infos()
    utils.populate_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
