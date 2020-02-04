from rest_framework import serializers

from StreamServerApp.models import Video, Series, Movie
from StreamServerApp.fields import PaginatedRelationField


class VideoSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(many=False)
    series = serializers.StringRelatedField(many=False)

    class Meta:
        model = Video
        fields = [
            'id', 
            'name', 
            'video_url', 
            'thumbnail', 
            'fr_subtitle_url', 
            'en_subtitle_url', 
            'ov_subtitle_url', 
            'series', 
            'movie', 
            'episode', 
            'season'
        ]


class SeriesListSerializer(serializers.ModelSerializer):
    """
    This serializer is used for listing series. 
    We do not list items from the video_set related field.
    """
    class Meta:
        model = Series
        fields = ['id', 'title']


class SeriesSerializer(serializers.ModelSerializer):
    """
    This serializer is used for retrieving a series. 
    We list items from the video_set related field, and the seasons.
    """
    video_set = PaginatedRelationField(VideoSerializer)
    seasons = serializers.ReadOnlyField(source='season_list')

    class Meta:
        model = Series
        fields = ['id', 'title', 'video_set', 'seasons']


class MoviesSerializer(serializers.ModelSerializer):
    video_set = PaginatedRelationField(VideoSerializer)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'video_set']
