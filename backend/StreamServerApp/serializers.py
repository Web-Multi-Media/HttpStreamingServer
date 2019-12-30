from StreamServerApp.models import Video
from rest_framework import serializers


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'name', 'video_url', 'thumbnail', 'fr_subtitle_url', 'en_subtitle_url', 'ov_subtitle_url']