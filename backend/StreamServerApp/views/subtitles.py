
from rest_framework import viewsets, generics
from StreamServerApp.serializers.subtitles import SubtitleListSerializer
from StreamServerApp.models import Subtitle


class SubtitleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `search` actions for Videos
    """

    def _allowed_methods(self):
        return ['GET']

    def get_serializer_class(self):
        """
        Overwirte
        """
        if self.action == 'list':
            return SubtitleListSerializer
        elif self.action == 'retrieve':
            return SubtitleListSerializer

    def get_queryset(self):
        """
        Optionally performs search on the series, by using the `search_query`
        query parameter in the URL.
        """
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            queryset = Subtitle.objects.search_trigramm('title', search_query)
        else:
            queryset = Subtitle.objects.all()
        return queryset
