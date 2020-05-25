from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'videos', views.VideoViewSet, basename='videos')
router.register(r'series', views.SeriesViewSet, basename='series')
router.register(r'movies', views.MoviesViewSet, basename='movie')


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^', include(router.urls)),
    url('^series/(?P<series>.+)/season/(?P<season>.+)$', views.SeriesSeaonViewSet.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]
