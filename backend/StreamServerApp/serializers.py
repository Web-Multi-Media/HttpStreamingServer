from rest_framework import serializers

from StreamServerApp.models import Video, Series
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


class SeriesSerializer(serializers.ModelSerializer):
    video_set = PaginatedRelationField(VideoSerializer)
    seasons = serializers.ReadOnlyField(source='return_season_list')

    class Meta:
        model = Series
        fields = ['id', 'title', 'video_set', 'seasons']
