import traceback
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from StreamServerApp.models import Subtitle
from StreamServerApp.fields import PaginatedRelationField


class SubtitleListSerializer(serializers.ModelSerializer):

    video_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Subtitle
        fields = [
            'id', 
            'webvtt_subtitle_url', 
            'language', 
            'video_id', 
        ]
