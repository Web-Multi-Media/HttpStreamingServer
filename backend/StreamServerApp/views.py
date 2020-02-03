import json
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.postgres.search import TrigramSimilarity
from django.core import serializers
from django.core.paginator import Paginator
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics

from StreamServerApp.serializers import VideoSerializer, SeriesSerializer, MoviesSerializer
from StreamServerApp.models import Video, Series, Movie
from StreamServerApp import utils


def index(request):
    return render(request, "index.html")


class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Videos
    """
    serializer_class = VideoSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        
        videoname = self.request.query_params.get('search_query', None)
        if videoname:
            queryset = Video.objects.search_trigramm('name', videoname)
        else:
            queryset = Video.objects.all()
        return queryset


class SeriesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Series
    """
    serializer_class = SeriesSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        
        seriesname = self.request.query_params.get('search_query', None)
        if seriesname:
            queryset = Series.objects.search_trigramm('title', seriesname)
        else:
            queryset = Series.objects.all()
        return queryset


class SeriesSeaonViewSet(generics.ListAPIView):
    """
    This viewset provides listing of episodes of a season of a series.
    """
    serializer_class = VideoSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_queryset(self):
        series_pk = int(self.kwargs['series'])
        season_number = int(self.kwargs['season'])

        return Series.objects.get(pk=series_pk).return_season_episodes(season_number)

class MoviesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Series
    """
    serializer_class = MoviesSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        
        seriesname = self.request.query_params.get('search_query', None)
        if seriesname:
            queryset = Movie.objects.search_trigramm('title', seriesname)
        else:
            queryset = Movie.objects.all()
        return queryset
        