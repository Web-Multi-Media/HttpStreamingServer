from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from StreamServerApp.views import update

urlpatterns = [
    url(r'^updatedb/', update.RestUpdate().as_view(), name='updatedb'),
]
