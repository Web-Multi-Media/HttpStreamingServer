import json
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.postgres.search import TrigramSimilarity
from django.core import serializers
from django.core.paginator import Paginator
from django.conf import settings

from StreamServerApp.serializers import VideoSerializer

from StreamServerApp.models import Video
from StreamServerApp import utils
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters


def index(request):
    return render(request, "index.html")

class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Videos
    """
    serializer_class = VideoSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Video.objects.all()
        videoname = self.request.query_params.get('name', None)
        if videoname is not None:
            queryset = Video.objects.annotate(similarity=TrigramSimilarity('name', videoname)) \
            .filter(similarity__gte=0.01) \
            .order_by('-similarity')
        return queryset
