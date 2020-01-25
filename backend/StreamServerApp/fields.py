from rest_framework.fields import Field
from rest_framework.settings import api_settings
from rest_framework import pagination
import re


# This custom pagination behaves the same as the default one but returns a dict instead of a Response object.
# It is used for paginating related fields of a model class (e.g. Series).
class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data, from_specific_instance):
        """Custom paginator
        from_specific_instance argument is used to display next and previous urls only when dealing with a 
        specific instance (e.g. series), but not when requesting many instances (e.g. series search).
        The pagination in nested results is not really possible.
        """
        if from_specific_instance:
            return {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
                'results': data
            }
        else:
            return {
                'count': self.page.paginator.count,
                'results': data,
            }


# Adapted from https://groups.google.com/forum/#!topic/django-rest-framework/QZ6-qmTMLcA
# It allows to paginate over related fields of class models (e.g. Series).
# It uses the custom paginator defined above.
class PaginatedRelationField(Field):
    def __init__(self, serializer, filters=None, paginator=CustomPagination, **kwargs):
        self.serializer = serializer
        self.paginator = paginator()

        # Filters should be a dict, for example: {'pk': 1}
        self.filters = filters

        super(PaginatedRelationField, self).__init__(**kwargs)

    def to_representation(self, related_objects):
        if self.filters:
            related_objects = related_objects.filter(**self.filters)

        request = self.context.get('request')
        
        # coming from /series/ or /series/<series_pk>/ ?
        #             /movies/ or /movie/<movie_pk>/   ?
        request_path = request.META['PATH_INFO']
        from_specific_instance = re.match(r'.*\/[a-z]+\/\d*\/', request_path) is not None

        serializer = self.serializer(
            related_objects, many=True, context={'request': request}
        )
        paginated_data = self.paginator.paginate_queryset(
            queryset=serializer.data, request=request
        )

        result = self.paginator.get_paginated_response(paginated_data, from_specific_instance)
        return result
        