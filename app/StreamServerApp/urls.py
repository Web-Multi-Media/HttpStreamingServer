from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url('get_videos/', views.get_videos, name="get-videos"),
    path('search_video/', views.search_video, name='search-video'),
    path('update_database/', views.update_database, name='update-database'),
]
