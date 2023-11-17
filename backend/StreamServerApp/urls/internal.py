from django.urls import re_path
from StreamServerApp.views import update

urlpatterns = [
    re_path(r'^updatedb/', update.RestUpdate().as_view(), name='updatedb'),
]
