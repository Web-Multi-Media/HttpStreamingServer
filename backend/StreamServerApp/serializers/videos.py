from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from StreamServerApp.models import Video, Series, Movie
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
    time = serializers.SerializerMethodField('get_video_time_history')

    def get_video_time_history(self, obj):
        user_token = self.context['request'].headers.get('Authorization')
        try:
            user = User.objects.get(auth_token=user_token)
            return obj.return_user_time_history(user)

        except ObjectDoesNotExist:
            print('User not found, token recieved: {}'.format(user_token))

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
