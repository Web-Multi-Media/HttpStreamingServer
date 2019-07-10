from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url('getallvideos/', views.getallvideos, name="getallvideos"),
    path('search_video/', views.search_video, name='search-video'),
]
