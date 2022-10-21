from django.contrib import admin
from StreamServerApp.models import Video, Movie, Series, Subtitle, delete_video_related_assets
from django.conf import settings
import os
import shutil




class VideoAdmin(admin.ModelAdmin):
    search_fields = ['name']
    model = Video

    def delete_queryset(self, request, queryset):
        print(
            '========================delete_queryset========================')
        print(queryset)
        for video in queryset:
            delete_video_related_assets(video)
        queryset.delete()


class SeriesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    model = Series

    def delete_queryset(self, request, queryset):
        print(
            '========================delete_queryset========================')
        print(queryset)
        #queryset.delete()
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
        print(
            '========================delete_queryset========================')
        print(queryset)
        #queryset.delete()
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
