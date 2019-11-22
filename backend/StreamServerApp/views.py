import json
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
    page = request.GET.get('page', 1)
    qs = Video.objects.all()

    results = paginate_and_serialize_results(qs, page)

    return HttpResponse(results, content_type='application/json')


def search_video(request):
    print(request)
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    if query == '':
        qs_results = Video.objects.all()
    else:
        qs_results = Video.objects.annotate(similarity=TrigramSimilarity('name', query)) \
                                .filter(similarity__gte=0.01) \
                                .order_by('-similarity')

    results = paginate_and_serialize_results(qs_results, page)

    return HttpResponse(results, content_type='application/json')


def paginate_and_serialize_results(query_set, page=1):
    """Extract a page and serialize the results.

    This methods aims at facilitating the reuse of our pagination and serialization in the different views.
    For now, we use a hacky technique (serialize, unserialize, add field, reserialize) in order to add the 
    informations of the number of results and number of pages.

    Args:
        query_set (QuerySet): QuerySet instance of retrieved results.
        page (int): page number requested.

    Returns:
        str: serialized json string containing the results and informations about the search.
    """
    paginator = Paginator(query_set, settings.PAGE_SIZE)
    results = paginator.get_page(page)
    results_json = serializers.serialize('json', results)
    results_dict = json.loads(results_json)
    output_dict = {
        'num_results': paginator.count,
        'num_pages': paginator.num_pages,
        'results': results_dict
    }
    return json.dumps(output_dict)
    

def update_database(request):
    print("updating database")
    utils.delete_DB_Infos()
    utils.populate_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
