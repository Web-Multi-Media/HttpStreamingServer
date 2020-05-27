from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from StreamServerApp.serializers.videos import ExtendedVideoSerializer, SimpleVideoSerializer, \
     SeriesSerializer, MoviesSerializer, SeriesListSerializer
from StreamServerApp.models import Video, Series, Movie
from StreamServerApp import utils


def index(request):
    return render(request, "index.html")


class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Videos
    """

    def _allowed_methods(self):
        return ['GET']

    def get_serializer_class(self):
        """
        Overwirte
        """
        if self.action == 'list':
            return SimpleVideoSerializer
        if self.action == 'retrieve':
            return ExtendedVideoSerializer

    def get_queryset(self):
        """
        Optionally performs search on the videos, by using the `search_query` 
        query parameter in the URL.
        """
        
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            queryset = Video.objects.search_trigramm('name', search_query)
        else:
            queryset = Video.objects.all()
        return queryset


class SeriesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Series
    """

    def _allowed_methods(self):
        return ['GET']

    def get_serializer_class(self):
        """
        Overwirte 
        """
        if self.action == 'list':
            return SeriesListSerializer
        if self.action == 'retrieve':
            return SeriesSerializer          

    def get_queryset(self):
        """
        Optionally performs search on the series, by using the `search_query` 
        query parameter in the URL.
        """
        print(self.request.user)
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            queryset = Series.objects.search_trigramm('title', search_query)
        else:
            queryset = Series.objects.all()
        return queryset


class SeriesSeaonViewSet(generics.ListAPIView):
    """
    This viewset provides listing of episodes of a season of a series.
    """
    serializer_class = ExtendedVideoSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_queryset(self):
        series_pk = int(self.kwargs['series'])
        season_number = int(self.kwargs['season'])

        return Series.objects.get(pk=series_pk).return_season_episodes(season_number)


class MoviesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Movies
    """
    serializer_class = MoviesSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_queryset(self):
        """
        Optionally performs search on the movies, by using the `search_query` 
        query parameter in the URL.
        """
        
        seriesname = self.request.query_params.get('search_query', None)
        if seriesname:
            queryset = Movie.objects.search_trigramm('title', seriesname)
        else:
            queryset = Movie.objects.all()
        return queryset
