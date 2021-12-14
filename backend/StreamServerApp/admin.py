from django.contrib import admin
from StreamServerApp.models import Video, Movie, Series, Subtitle
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
        #queryset.delete()
        for videos in queryset:
            print(videos.video_folder)
            playlistdir = os.path.split(videos.video_folder)[0]
            if os.path.isdir(playlistdir):
                print("removing directory: {}".format(playlistdir))
                shutil.rmtree(playlistdir, ignore_errors=True)

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
            for videos in video_queryset:
                playlistdir = os.path.split(videos.video_folder)[0]
                if os.path.isdir(playlistdir):
                    print("removing directory: {}".format(playlistdir))
                    shutil.rmtree(playlistdir, ignore_errors=True)
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
            for videos in video_queryset:
                playlistdir = os.path.split(videos.video_folder)[0]
                if os.path.isdir(playlistdir):
                    print("removing directory: {}".format(playlistdir))
                    shutil.rmtree(playlistdir, ignore_errors=True)
            video_queryset.delete()

        queryset.delete()


admin.site.register(Video, VideoAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Subtitle)
