from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User

from StreamServerApp.serializers.videos import ExtendedVideoSerializer
from StreamServerApp.models import Video, UserVideoHistory


class History(APIView):
    """
    Get, create and update user history
    """
    def get(self, request):
        user_token = request.headers.get('Authorization')
        user = User.objects.get(auth_token=user_token)

        queryset = Video.objects.filter(history=user).order_by('-uservideohistory__updated_at')
        serializer = ExtendedVideoSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        user_token = request.data.get('headers').get('Authorization')
        video_id = request.data.get('body').get('video-id')
        time = request.data.get('body').get('video-time', 0)
        print(user_token)
        user = User.objects.get(auth_token=user_token)
        video = Video.objects.get(id=video_id)

        history, created = UserVideoHistory.objects.get_or_create(
            user=user,
            video=video,
            defaults={'time': time},
        )

        if not created:
            history.time = time
            history.save()

        return Response({}, status=status.HTTP_200_OK)
