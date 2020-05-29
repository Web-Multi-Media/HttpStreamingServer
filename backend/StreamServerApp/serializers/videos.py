import traceback
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from StreamServerApp.models import Video, Series, Movie
from StreamServerApp.fields import PaginatedRelationField


class VideoSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(many=False)
    series = serializers.StringRelatedField(many=False)
    time = serializers.SerializerMethodField('get_video_time_history')

    def get_video_time_history(self, obj):
        if self.context['request'].method == 'GET':
            user_token = self.context['request'].headers.get('Authorization')
        elif self.context['request'].method == 'POST':
            user_token = self.context['request'].data.get('headers').get('Authorization')

        try:
            user = User.objects.get(auth_token=user_token)
            return obj.return_user_time_history(user)

        except ObjectDoesNotExist as ex:
            print('User not found, token recieved: {}'.format(user_token))
            traceback.print_exception(type(ex), ex, ex.__traceback__)

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
