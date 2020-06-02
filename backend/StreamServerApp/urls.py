from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import videos
from .views import accounts


router = DefaultRouter()
router.register(r'videos', videos.VideoViewSet, basename='videos')
router.register(r'series', videos.SeriesViewSet, basename='series')
router.register(r'movies', videos.MoviesViewSet, basename='movies')
# router.register(r'history', accounts.HistoryViewSet, basename='history')


urlpatterns = [
    path('', videos.index, name='index'),
    url(r'^', include(router.urls)),
    url('^series/(?P<series>.+)/season/(?P<season>.+)/$', videos.SeriesSeaonViewSet.as_view()),
    url(r'^history/', accounts.History.as_view(), name='history'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]
