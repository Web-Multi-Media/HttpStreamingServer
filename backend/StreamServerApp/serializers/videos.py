from rest_framework import serializers

from StreamServerApp.models.videos import Video, Series, Movie
from StreamServerApp.fields import PaginatedRelationField


class SimpleVideoSerializer(serializers.ModelSerializer):
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
            'season',
        ]

class ExtendedVideoSerializer(serializers.ModelSerializer):
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
            'season',
            'next_episode',
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
    video_set = PaginatedRelationField(ExtendedVideoSerializer)
    seasons = serializers.ReadOnlyField(source='season_list')

    class Meta:
        model = Series
        fields = ['id', 'title', 'video_set', 'seasons']


class MoviesSerializer(serializers.ModelSerializer):
    video_set = PaginatedRelationField(SimpleVideoSerializer)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'video_set']
