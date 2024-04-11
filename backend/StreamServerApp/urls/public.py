from django.urls import path, re_path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from StreamServerApp.views import videos, subtitles, tasks, update, accounts


router = DefaultRouter()
router.register(r'videos', videos.VideoViewSet, basename='videos')
router.register(r'series', videos.SeriesViewSet, basename='series')
router.register(r'movies', videos.MoviesViewSet, basename='movies')
router.register(r'subtitles', subtitles.SubtitleViewSet, basename='subtitles')


urlpatterns = [
    path('', videos.index, name='index'),
    re_path(r'^', include(router.urls)),
    re_path('^series/(?P<series>.+)/season/(?P<season>.+)/$', videos.SeriesSeaonViewSet.as_view()),
    re_path(r'^history/', accounts.History.as_view(), name='history'),
    re_path(r'^updatedb/', update.RestUpdate().as_view(), name='updatedb'),
    re_path(r'^tasks/(?P<task_id>.+)/$', tasks.Task.as_view(), name='task'),
    re_path(r'^rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^sync_subtitles/(?P<video_id>.+)/(?P<subtitle_id>.+)/$', videos.request_sync_subtitles)
]

urlpatterns_internal = [
     re_path(r'^updatedb/', update.RestUpdate.as_view(), name='updatedb'),
]

