from django.apps import AppConfig
from rest_framework.permissions import BasePermission


class StreamserverappConfig(AppConfig):
    name = 'StreamServerApp'


class IsStaff(BasePermission):
    """ Permission used for all views
    We check if the api user is staff for granting permission.
    """
    def has_permission(self, request, view):
        if hasattr(request, 'api_user'):
            return request.api_user.is_staff
        else:
            return False
