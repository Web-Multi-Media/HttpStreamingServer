from django.contrib import admin
from StreamServerApp.models import Video, Movie, Series, Subtitle, delete_video_related_assets
from django.conf import settings
import os
import shutil
from django.contrib.auth.admin import UserAdmin




class VideoAdmin(admin.ModelAdmin):
    search_fields = ['name']
    model = Video
    list_display = ["name", "video_folder_size_in_MB"]

    def delete_queryset(self, request, queryset):
        for video in queryset:
            delete_video_related_assets(video)
        queryset.delete()


class SeriesAdmin(admin.ModelAdmin):
    search_fields = ['title']
    model = Series
    list_display = ["title", "size_in_mb"]

    def delete_queryset(self, request, queryset):
        for series in queryset:
            video_queryset = Video.objects.filter(series=series.id)
            for video in video_queryset:
                delete_video_related_assets(video)
            video_queryset.delete()

        queryset.delete()


class MovieAdmin(admin.ModelAdmin):
    search_fields = ['name']
    model = Movie

    def delete_queryset(self, request, queryset):
        for movies in queryset:
            video_queryset = Video.objects.filter(movie=movies.id)
            for video in video_queryset:
                delete_video_related_assets(video)
            video_queryset.delete()

        queryset.delete()


admin.site.register(Video, VideoAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Subtitle)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
