import traceback
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination

from StreamServerApp.serializers.videos import ExtendedVideoSerializer
from StreamServerApp.models import Video, UserVideoHistory


class History(APIView, LimitOffsetPagination):
    """
    Get, create and update user history
    """
    def get_history(self, request, user_token):
        user = User.objects.get(auth_token=user_token)
        queryset = Video.objects.filter(history=user).order_by('-uservideohistory__updated_at')
        results = self.paginate_queryset(queryset, request, view=self)
        serializer = ExtendedVideoSerializer(results, many=True, context={"request": self.request})
        return self.get_paginated_response(serializer.data)

    def get(self, request):
        try:
            user_token = request.headers.get('Authorization')
            return self.get_history(request, user_token)

        except ObjectDoesNotExist:
            print('User not found, token recieved: {}'.format(user_token))
            return Response({'error': 'Check the user token!'}, status=status.HTTP_404_NOT_FOUND)
        except:
            traceback.print_exc()
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            user_token = request.data.get('headers').get('Authorization')
            video_id = request.data.get('body').get('video-id')
            time = request.data.get('body').get('video-time', 0)
            user = User.objects.get(auth_token=user_token)
            video = Video.objects.get(id=video_id)

            # For series we only keep one video history
            if video.series:
                UserVideoHistory.objects.filter(user=user, video__series=video.series).delete()
            
            # We still get or create here because there can be existing movie histories
            history, created = UserVideoHistory.objects.get_or_create(
                user=user,
                video=video,
                defaults={'time': time},
            )

            # We update the time when recieving new history for an existing history
            if not created:
                history.time = time
                history.save()

            # We send the history back to the client
            return self.get_history(request, user_token)

        except ObjectDoesNotExist:
            print('User not found, token recieved: {}'.format(user_token))
            return Response({'error': 'Check the user token!'}, status=status.HTTP_404_NOT_FOUND)
        except:
            traceback.print_exc()
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
