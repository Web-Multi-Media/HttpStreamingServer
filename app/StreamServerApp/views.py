from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from StreamServerApp.models import Video
from django.contrib.postgres.search import TrigramSimilarity


def index(request):
    template = loader.get_template('StreamServerApp/index.html')
    return HttpResponse(template.render({}, request))

def rendervideo(request):
    vid_number_str = request.GET.get('VideoNumber')
    context = {}
    pks = list(Video.objects.values_list('pk', flat=True))
    if (len(pks) == 0):
        print("ERROR: Database is not loaded")
        raise Http404("Database is not loaded")
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
    return JsonResponse(context)


def search_video(request):
    query = request.GET.get('q', '')

    # ANOTHER EXAMPLE:
    # vector = SearchVector('name', weight='A') + SearchVector('description', weight='C')
    # query = SearchQuery(query)
    # qs_results = TaxonomyNode.objects.filter(taxonomy__dataset=dataset)\
    #                                  .annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3)\
    #                                  .order_by('rank')

    qs_results = Video.objects.annotate(similarity=TrigramSimilarity('name', query)) \
                              .filter(similarity__gte=0.2) \
                              .order_by('-similarity')

    results = qs_results.values('name', 'baseurl', 'id')

    return JsonResponse(list(results[:10]), safe=False)


