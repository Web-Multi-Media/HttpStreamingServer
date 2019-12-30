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


def index(request):
    return render(request, "index.html")

class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
