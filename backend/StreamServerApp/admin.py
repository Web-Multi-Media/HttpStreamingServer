from django.contrib import admin
from StreamServerApp.models.videos import Video
from StreamServerApp.utils import delete_DB_Infos, populate_db_from_local_folder
from django.conf import settings


def reload_video(modeladmin, request, queryset):
    delete_DB_Infos()
    populate_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
    reload_video.short_description = "Reload videos"

class VideoAdmin(admin.ModelAdmin):
    actions = []

admin.site.register(Video, VideoAdmin)
admin.site.add_action(reload_video)