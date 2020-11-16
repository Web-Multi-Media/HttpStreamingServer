from django.contrib import admin
from StreamServerApp.models import Video, Movie, Series, Subtitle
from StreamServerApp.database_utils import delete_DB_Infos, populate_db_from_local_folder, update_db_from_local_folder
from django.conf import settings


def populate_videos(modeladmin, request, queryset):
    delete_DB_Infos()
    populate_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
    populate_videos.short_description = "Populate videos database"


def update_videos(modeladmin, request, queryset):
    update_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
    update_videos.short_description = "Update videos database"


class VideoAdmin(admin.ModelAdmin):
    actions = []


admin.site.register(Video, VideoAdmin)
admin.site.register(Movie, VideoAdmin)
admin.site.register(Series, VideoAdmin)
admin.site.register(Subtitle, VideoAdmin)
admin.site.add_action(populate_videos)
admin.site.add_action(update_videos)
