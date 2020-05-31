from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from StreamServerApp.serializers.videos import VideoSerializer, \
     SeriesSerializer, MoviesSerializer, SeriesListSerializer
from StreamServerApp.models import Video, Series, Movie, User
from StreamServerApp import utils


def index(request):
    return render(request, "index.html")


def get_authenticated_user(request):
    """
    Returns the user instance from the databse.

    It is used here to add the user in the request so we can get it from the serializer,
    ideally it should be done in a middleware...
    """
    if request.method == 'GET':
        user_token = request.headers.get('Authorization')
    elif request.method == 'POST':
        user_token = request.data.get('headers').get('Authorization')

    if user_token:
        user = User.objects.get(auth_token=user_token)
        return user
    

class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Videos
    """
    serializer_class = VideoSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_serializer_context(self):
        context = super(VideoViewSet, self).get_serializer_context()
        user = get_authenticated_user(self.request)
        self.request.user = user  # ideally this should be done in a middleware
        context.update({"request": self.request})
        return context

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
    serializer_class = VideoSerializer

    def _allowed_methods(self):
        return ['GET']

    def get_serializer_context(self):
        context = super(SeriesSeaonViewSet, self).get_serializer_context()
        user = get_authenticated_user(self.request)
        self.request.user = user  # ideally this should be done in a middleware
        context.update({"request": self.request})
        return context

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

    def get_serializer_context(self):
        context = super(MoviesViewSet, self).get_serializer_context()
        user = get_authenticated_user(self.request)
        self.request.user = user  # ideally this should be done in a middleware
        context.update({"request": self.request})
        return context

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
