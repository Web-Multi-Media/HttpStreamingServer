from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.models import User

from StreamServerApp.serializers.videos import ExtendedVideoSerializer
from StreamServerApp.models import Video, UserVideoHistory


# class HistoryViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides 
#     """

#     permission_classes = (IsAuthenticated,)

#     queryset = Video.objects.all()
#     serializer_class = ExtendedVideoSerializer

#     def _allowed_methods(self):
#         return ['GET', 'POST']


class History(APIView):
    """
    Get, create and update user history
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        user_token = request.data.get('token')
        user = User.objects.get(auth_token=user_token)

        queryset = Video.objects.filter(history__user=user).order_by('-updated_at')
        serializer = ExtendedVideoSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        user_token = request.data.get('token')
        video_id = request.data.get('video-id')
        time = request.data.get('video-time', 0)

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
