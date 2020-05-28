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
    def get(self, request):
        try:
            user_token = request.headers.get('Authorization')
            user = User.objects.get(auth_token=user_token)
            queryset = Video.objects.filter(history=user).order_by('-uservideohistory__updated_at')
            results = self.paginate_queryset(queryset, request, view=self)
            serializer = ExtendedVideoSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

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

            history, created = UserVideoHistory.objects.get_or_create(
                user=user,
                video=video,
                defaults={'time': time},
            )

            if not created:
                history.time = time
                history.save()

            return Response({}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            print('User not found, token recieved: {}'.format(user_token))
            return Response({'error': 'Check the user token!'}, status=status.HTTP_404_NOT_FOUND)
        except:
            traceback.print_exc()
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
