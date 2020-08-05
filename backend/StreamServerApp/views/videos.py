import os
from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from StreamServerApp.tasks import sync_subtitles
from StreamServerApp.serializers.videos import VideoSerializer, \
     SeriesSerializer, MoviesSerializer, SeriesListSerializer, VideoListSerializer
from StreamServerApp.models import Video, Series, Movie
import subprocess


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
            return VideoListSerializer
        if self.action == 'retrieve':
            return VideoSerializer   

    def get_queryset(self):
        """
        Optionally performs search on the videos, by using the `search_query` 
        query parameter in the URL.
        """
        
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            queryset = Video.objects.search_trigramm('name', search_query).select_related('movie', 'series')
        else:
            queryset = Video.objects.select_related('movie', 'series').all()
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
    serializer_class = VideoListSerializer

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
        
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            queryset = Movie.objects.search_trigramm('title', search_query).prefetch_related('video_set')
        else:
            queryset = Movie.objects.prefetch_related('video_set').all()
        return queryset


def request_sync_subtitles(request, video_id,language):
    video = Video.objects.get(id=video_id)
    video_path = os.path.join(video.video_folder, video.name)
    if (language == 'en') :
        subtitles_path = os.path.join(video.video_folder, video.en_srt_subtitle_url.replace(video.video_url.replace(video.name,''),''))
        webvtt_path = os.path.join(video.video_folder, video.en_webvtt_subtitle_url.replace(video.video_url.replace(video.name,''),''))
    if (language == 'fr') :
        subtitles_path = os.path.join(video.video_folder, video.fr_srt_subtitle_url.replace(video.video_url.replace(video.name,''),''))
        webvtt_path = os.path.join(video.video_folder, video.fr_webvtt_subtitle_url.replace(video.video_url.replace(video.name,''),''))
    webvtt_path = webvtt_path.replace('.vtt','_sync.vtt')
    sync_subtitle_path = subtitles_path.replace('.srt','_sync.srt')
    sync_subtitles.delay(language,video_path,video_id,subtitles_path,sync_subtitle_path,webvtt_path)
