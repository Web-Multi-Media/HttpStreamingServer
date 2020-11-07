
from rest_framework import viewsets, generics
from StreamServerApp.serializers.subtitles import SubtitleListSerializer
from StreamServerApp.models import Subtitle


class SubtitleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Videos
    """

    queryset = Subtitle.objects.all()
    serializer_class = SubtitleListSerializer

    def _allowed_methods(self):
        return ['GET', 'POST']

    def perform_create(self, serializer):
        serializer.save(uploaded_data=self.request.data.get('datafile'))


