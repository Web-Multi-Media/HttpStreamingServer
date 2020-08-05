import traceback
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from StreamServerApp.models import Video, Series, Movie
from StreamServerApp.fields import PaginatedRelationField


class VideoListSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(many=False)
    series = serializers.StringRelatedField(many=False)

    class Meta:
        model = Video
        fields = [
            'id', 
            'name', 
            'video_url', 
            'thumbnail', 
            'fr_webvtt_subtitle_url', 
            'en_webvtt_subtitle_url',
            'fr_webvtt_sync_url',
            'en_webvtt_sync_url', 
            'ov_subtitle_url', 
            'series', 
            'movie', 
            'episode', 
            'season',
        ]


class VideoSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(many=False)
    series = serializers.StringRelatedField(many=False)
    time = serializers.SerializerMethodField('get_video_time_history')

    def get_video_time_history(self, obj):
        try:
            user = self.context['request'].api_user
            return obj.return_user_time_history(user)
        except:
            pass

    class Meta:
        model = Video
        fields = [
            'id', 
            'name', 
            'video_url', 
            'thumbnail', 
            'fr_webvtt_subtitle_url', 
            'en_webvtt_subtitle_url', 
            'ov_subtitle_url',
            'series', 
            'movie', 
            'episode', 
            'season',
            'next_episode',
            'time',
        ]


class SeriesListSerializer(serializers.ModelSerializer):
    """
    This serializer is used for listing series. 
    We do not list items from the video_set related field.
    """
    class Meta:
        model = Series
        fields = ['id', 'title', 'thumbnail']


class SeriesSerializer(serializers.ModelSerializer):
    """
    This serializer is used for retrieving a series. 
    We list items from the video_set related field, and the seasons.
    """
    seasons = serializers.ReadOnlyField(source='season_list')

    class Meta:
        model = Series
        fields = ['id', 'title', 'seasons']


class MoviesSerializer(serializers.ModelSerializer):
    video_set = PaginatedRelationField(VideoListSerializer)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'video_set']
