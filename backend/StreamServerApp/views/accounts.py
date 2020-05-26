from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from StreamServerApp.serializers.videos import ExtendedVideoSerializer
from StreamServerApp.models.videos import Video


class HistoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 
    """

    permission_classes = (IsAuthenticated,)

    queryset = Video.objects.all()
    serializer_class = ExtendedVideoSerializer

    def _allowed_methods(self):
        return ['GET', 'POST']
