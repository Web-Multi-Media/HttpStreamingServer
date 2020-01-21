from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'videos', views.VideoViewSet, basename='videos')
router.register(r'series', views.SeriesViewSet, basename='series')


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^', include(router.urls)),
]
