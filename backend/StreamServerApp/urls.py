from django.urls import path
from django.conf.urls import url

from . import views

video_list = views.VideoViewSet.as_view({
    'get': 'list',
})

video_detail = views.VideoViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('', views.index, name='index'),
    path('videos/', video_list, name="video-list"),
    path('videos/<int:video_id>/', video_detail, name="video-detail"),
    #path('search_video/', views.search_video, name='search-video'),
]
